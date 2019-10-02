# AWS Callouts

This project is a tools to send out bound call reminder with AWS Connect and save the confirmation record in DynamoDB.


## Setup

1. Deploy ExcelLexBot.
2. Upload CalloutBot.xlsx to the S3 bucket for ExcelLexBot.
2. You have to create a AWS connect instance with a contact flow. https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html 
2. Import contract_flow/CallingOutContractFlow.json . https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html
3. Deploy this project.

## Deployment with Cloud9
Update ContactFlowArn, and SourcePhoneNumber in deployment.sh.

./setup.sh

sudo ./get_layer_packages.sh

./deployment.sh


## Sample Code to make calls

```python
import boto3
import json

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(
    QueueName="it114115callout-CallSqsQueue-54UT6EDQV492")

call1 = {"id": "001", "username": "Lee Wang", "phone_number": "+85212345888"}

call2 = {"id": "002", "username": "Cyrus Wong", "phone_number": "+85212345678"}

call_list = [call1, call2]

call_task = {
    "task_id": "Calling",
    "message_template": "Hi {{ username }}, This is a test!",
    "receivers": call_list
}

response = queue.send_message(MessageBody=json.dumps(call_task))

print(response)


```

