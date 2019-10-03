import boto3

sqs = boto3.client('sqs')


def delete_message_batch(sqs_queue_url: str, event):
    receiptHandles = list(
        map(
            lambda record: {
                "Id": record["messageId"],
                "ReceiptHandle": record["receiptHandle"]
            }, event['Records']))
    response = sqs.delete_message_batch(QueueUrl=sqs_queue_url,
                                        Entries=receiptHandles)
    return response
