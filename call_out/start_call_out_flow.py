import os
import datetime
import json
import logging
import math
import random
import boto3
from botocore.exceptions import ClientError

from sqs_helper import *

stepfunctions = boto3.client('stepfunctions')
sqs = boto3.client('sqs')

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s: %(message)s')

maximum_parallel_call = 20


def lambda_handler(event, context):
    print(event)

    call_task = json.loads(event['Records'][0]['body'])
    data = body_transform(call_task)
    print(data)

    results = list(
        map(
            lambda call: put_object(
                os.environ['ExcelCallJobBucket'], call_task['task_id'] + "/" +
                call["id"] + ".json", json.dumps(call)), data))

    keys = list(
        map(lambda call: call_task['task_id'] + "/" + call["id"] + ".json",
            data))

    name = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + "-callout"
    response = stepfunctions.start_execution(
        stateMachineArn=os.environ['CalloutStateMachineArn'],
        name=name,
        input=json.dumps(keys))

    delete_message_batch(os.environ['CallSqsQueueUrl'], event)
    return response


def put_object(dest_bucket_name, dest_object_name, object_data):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=dest_bucket_name,
                      Key=dest_object_name,
                      Body=object_data)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def body_transform(call_task):
    def add_fields(receiver, fields):
        receiver.update(fields)
        return receiver

    return list(
        map(
            lambda receiver: add_fields(
                receiver, {
                    'task_id':
                    call_task['task_id'],
                    'status':
                    "DropCall",
                    "greeting":
                    call_task['greeting'],
                    "ending":
                    call_task['ending'],
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
                    "delay":
                    random.randrange(
                        0,
                        math.ceil(
                            len(call_task["receivers"]) / maximum_parallel_call
                        ) + 1),
                    'call_at':
                    datetime.datetime.utcnow().isoformat()
                }), call_task["receivers"]))
