import os
import boto3
import botocore
import json

from sqs_helper import *

client = boto3.client('connect')
stepfunctions_client = boto3.client("stepfunctions")

def lambda_handler(event, context):

    contract_flow_arn = os.environ['ContactFlowArn']
    instance_id = contract_flow_arn.split("/")[1]
    contract_flow_id = contract_flow_arn.split("/")[3]

    body = json.loads(event["Records"][0]["body"])
    print(body)
    message = body['Message']
    message['taskToken']=body["TaskToken"]
    print(message)

    delete_message_batch(os.environ['AsynCalloutQueueUrl'], event)
    try:
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=message['phone_number'],
            ContactFlowId=contract_flow_id,
            InstanceId=instance_id,
            SourcePhoneNumber=os.environ['SourcePhoneNumber'],
            Attributes=message)
    except Exception as err:
        print(err)
        event['status'] = "NotCallable"
        event['error'] = str(err)
        
        print(f"Sending task failure for task ID {message['taskToken']}")
        stepfunctions_client.send_task_success(
            taskToken=message["taskToken"],
            output=json.dumps(event)
        )
        return event

                                 
                                        
    event['status'] = "Calling"
    return event
