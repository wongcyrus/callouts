# AWS Callouts

This project is a tools to send out bound call reminder with AWS Connect and save the confirmation record in DynamoDB.


## Setup

1. Deploy ExcelLexBot.
2. Upload CalloutBot.xlsx to the S3 bucket for ExcelLexBot.
3. You have to create a AWS connect instance with a contact flow. https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html 
4. Import contract_flow/CallingOutContractFlow.json . https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html
5. Update the Contact flows to access Lex Chatbot CalloutBot_ExcelLexBot
6. Deploy this project.

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

test_phone_list = ["39282662", "12345678"]

task_id = "call_test"
call_list = [{
    "id": task_id + "_" + str(i),
    "username": "Student_" + str(i),
    'phone_number': "+852" + phone_number
} for i, phone_number in enumerate(test_phone_list)]

call_task = {
    "task_id": task_id,
    "question_type": "Yes/No",  # OK, Yes/No, Multiple Choice
    "message_template": "Hi {{ username }}, Will you attend tomorrow class?",
    "receivers": call_list
}

print(call_task)
response = queue.send_message(MessageBody=json.dumps(call_task))

print(response)

```

