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
            Attributes=event)
    except Exception as err:
        print(err)
        event['status'] = "NotCallable"
        event['error'] = str(err)
        return event

    event['status'] = "Calling"
    return event
