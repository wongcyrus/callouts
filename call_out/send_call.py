import os
import boto3
import botocore
client = boto3.client('connect')


def lambda_handler(event, context):

    contract_flow_arn = os.environ['ContactFlowArn']
    instance_id = contract_flow_arn.split("/")[1]
    contract_flow_id = contract_flow_arn.split("/")[3]

    try:
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=event['phone_number'],
            ContactFlowId=contract_flow_id,
            InstanceId=instance_id,
            SourcePhoneNumber=os.environ['SourcePhoneNumber'],
            Attributes={
                'username': event['username'],
                'message': event['message']
            })
    except Exception as err:
        print(err)
        return {
            'username': event['username'],
            'message': event['message'],
            'phone_number': event['phone_number'],
            "status": "NotCallable",
            "error": str(err)
        }

    return {
        'username': event['username'],
        'message': event['message'],
        'phone_number': event['phone_number'],
        "status": "Calling"
    }
