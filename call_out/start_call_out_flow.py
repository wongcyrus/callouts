import os
import datetime
import json
import boto3
stepfunctions = boto3.client('stepfunctions')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    print(event)
    receiptHandles = list(
        map(
            lambda record: {
                "Id": record["messageId"],
                "ReceiptHandle": record["receiptHandle"]
            }, event['Records']))
    data = list(
        map(
            lambda record: {
                "messageId": record["messageId"],
                "body": record["body"]
            }, event['Records']))

    name = '{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + "-callout"
    response = stepfunctions.start_execution(
        stateMachineArn=os.environ['CalloutStateMachineArn'],
        name=name,
        input=json.dumps(data))

    response = sqs.delete_message_batch(QueueUrl=os.environ['CallSqsQueueUrl'],
                                        Entries=receiptHandles)
