import os
import datetime
import json
import sys
sys.path.append("/opt/")
from jinja2 import Environment, BaseLoader
import boto3

from sqs_helper import *

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
                        'task_id':
                        call_task['task_id'],
                        'question_type':
                        call_task['question_type'],
                        'status':
                        "DropCall",
                        'response_intent':
                        "null",
                        "error":
                        "null",
                        'message':
                        get_personalized_message(template, recevier),
                        'response_hanlder_function_arn':
                        os.environ['ResponseHanlderFunctionArn']
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
