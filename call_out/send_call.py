import os
import boto3
import botocore
import json
import time

import sys
sys.path.append("/opt/")
from jinja2 import Environment, BaseLoader

from sqs_helper import *

client = boto3.client('connect')
stepfunctions_client = boto3.client("stepfunctions")
s3 = boto3.client('s3')


def lambda_handler(event, context):

    contract_flow_arn = os.environ['ContactFlowArn']
    instance_id = contract_flow_arn.split("/")[1]
    contract_flow_id = contract_flow_arn.split("/")[3]
    
    body = json.loads(event["Records"][0]["body"])
    print(body)
    receiver = body['Message']
    task_token = body["TaskToken"]
    receiver['taskToken']=task_token
    receiver['status'] = "DropCall"
    receiver['response_intent'] = "null"
    # You can only pass str into the start_outbound_voice_contact!
    receiver["questions"] = json.dumps(get_questions(receiver))
    receiver["i"] = "0"
    receiver["greeting"] = get_personalized_message(receiver["greeting"],
                                                    receiver)
    receiver["ending"] = get_personalized_message(receiver["ending"], receiver)

    delay = receiver["delay"];
    del receiver["delay"]
    delete_message_batch(os.environ['AsynCalloutQueueUrl'], event)
    
    source_phone_number = str(os.environ['SourcePhoneNumber']).replace(" ", "").replace("-", "")

    try:
        print("Sleep: " + str(delay))
        time.sleep(delay)
        print(event)
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=receiver['phone_number'],
            ContactFlowId=contract_flow_id,
            InstanceId=instance_id,
            SourcePhoneNumber=source_phone_number,
            Attributes=receiver)
        print(response)    
        
    except Exception as err:
        print(err)
        receiver['status'] = "NotCallable"
        receiver['error'] = str(err)
        del receiver["taskToken"]
        del receiver["response_hanlder_function_arn"]
        del receiver["iterator_function_arn"]
        del receiver["send_task_success_function_arn"]
        
        print(f"Sending task failure for task ID {task_token}")
        stepfunctions_client.send_task_success(
            taskToken=task_token,
            output=json.dumps(receiver)
        )
        return event
                                        
    event['status'] = "Calling"
    return event

def get_personalized_message(template, receiver):
    rtemplate = Environment(loader=BaseLoader).from_string(template)
    return "<speak>"+ rtemplate.render(**receiver) + "</speak>"

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