import os
import boto3
import botocore
import json

import sys
sys.path.append("/opt/")
from jinja2 import Environment, BaseLoader

from sqs_helper import *

client = boto3.client('connect')
stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):

    contract_flow_arn = os.environ['ContactFlowArn']
    instance_id = contract_flow_arn.split("/")[1]
    contract_flow_id = contract_flow_arn.split("/")[3]

    body = json.loads(event["Records"][0]["body"])
    print(body)
    recevier = body['Message']
    task_token = body["TaskToken"]
    recevier['taskToken']=task_token
    recevier['status'] = "DropCall"
    recevier['response_intent'] = "null"
    # You can only pass str into the start_outbound_voice_contact!
    recevier["questions"] = json.dumps(get_questions(recevier))
    recevier["i"] = "0"
    
    print(recevier)

    delete_message_batch(os.environ['AsynCalloutQueueUrl'], event)
    try:
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=recevier['phone_number'],
            ContactFlowId=contract_flow_id,
            InstanceId=instance_id,
            SourcePhoneNumber=os.environ['SourcePhoneNumber'],
            Attributes=recevier)
    except Exception as err:
        print(err)
        recevier['status'] = "NotCallable"
        recevier['error'] = str(err)
        del recevier['taskToken']
        del recevier['response_hanlder_function_arn']
        
        print(f"Sending task failure for task ID {task_token}")
        stepfunctions_client.send_task_success(
            taskToken=task_token,
            output=json.dumps(recevier)
        )
        return event
                                        
    event['status'] = "Calling"
    return event

def get_personalized_message(template, receiver):
    rtemplate = Environment(loader=BaseLoader).from_string(template)
    return rtemplate.render(**receiver)

def get_questions(receiver):
    print(receiver)
    print(type(receiver))
    questions = receiver["questions"]
    return list(
        map(
            lambda question: {
                "question_type":
                question["question_type"],
                "question":
                get_personalized_message(question["question_template"],
                                         receiver)
            }, questions))