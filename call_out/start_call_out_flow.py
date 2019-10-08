import os
import datetime
import json
import boto3

from sqs_helper import *

stepfunctions = boto3.client('stepfunctions')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    print(event)

    def add_fields(recevier, fields):
        recevier.update(fields)
        return recevier

    def body_transform(call_task):
        call_task = json.loads(call_task)
        return list(
            map(
                lambda recevier: add_fields(
                    recevier, {
                        'task_id':
                        call_task['task_id'],
                        'status':
                        "DropCall",
                        "answers":
                        "[]",
                        "error":
                        "null",
                        "questions":
                        call_task['questions'],
                        "number_of_question":
                        str(len(call_task['questions'])),
                        'response_hanlder_function_arn':
                        os.environ['ResponseHanlderFunctionArn'],
                        'iterator_function_arn':
                        os.environ['IteratorFunctionArn'],
                        "send_task_success_function_arn":
                        os.environ['SendTaskSuccessFunctionArn'],
                        'call_at':
                        datetime.datetime.utcnow().isoformat()
                    }), call_task["receivers"]))

    data = body_transform(event['Records'][0]['body'])
    print(data)

    name = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + "-callout"
    response = stepfunctions.start_execution(
        stateMachineArn=os.environ['CalloutStateMachineArn'],
        name=name,
        input=json.dumps(data))

    delete_message_batch(os.environ['CallSqsQueueUrl'], event)
    return response
