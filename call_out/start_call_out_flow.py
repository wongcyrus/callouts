import os
import datetime
import json
import sys
sys.path.append("/opt/")
from jinja2 import Environment, BaseLoader
import boto3

stepfunctions = boto3.client('stepfunctions')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    print(event)

    def get_personalized_message(template, receiver):
        rtemplate = Environment(loader=BaseLoader).from_string(template)
        return rtemplate.render(**receiver)

    def add_fields(recevier, fields):
        recevier.update(fields)
        return recevier

    def body_transform(call_task):
        call_task = json.loads(call_task)
        template = call_task['message_template']
        return list(
            map(
                lambda recevier: add_fields(
                    recevier, {
                        'task_id': call_task['task_id'],
                        'message': get_personalized_message(
                            template, recevier)
                    }), call_task["receivers"]))

    receiptHandles = list(
        map(
            lambda record: {
                "Id": record["messageId"],
                "ReceiptHandle": record["receiptHandle"]
            }, event['Records']))

    data = body_transform(event['Records'][0]['body'])

    print(data)

    name = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + "-callout"
    response = stepfunctions.start_execution(
        stateMachineArn=os.environ['CalloutStateMachineArn'],
        name=name,
        input=json.dumps(data))

    response = sqs.delete_message_batch(QueueUrl=os.environ['CallSqsQueueUrl'],
                                        Entries=receiptHandles)
