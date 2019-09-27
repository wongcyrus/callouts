import json
import os

import boto3
client = boto3.client('connect')


def lambda_handler(event, context):

    response = client.start_outbound_voice_contact(
        DestinationPhoneNumber=event['phone_number'],
        ContactFlowId=os.environ['ContactFlowId'],
        InstanceId=os.environ['InstanceId'],
        SourcePhoneNumber=os.environ['SourcePhoneNumber'],
        Attributes={
            'username': event['username'],
            'message': event['message']
        })
