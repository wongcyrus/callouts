#Callouts

This project is a tools to send out bound call reminder with AWS Connect and save the confirmation record in DynamoDB.


## Setup Overview

1. Deploy ExcelLexBot.
2. Upload 4 CalloutBotXXX.xlsx file into the S3 bucket for ExcelLexBot.
3. You have to create a AWS connect instance with a contact flow. https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html 
4. Import contract_flow/CallingOutContractFlow.json . https://docs.aws.amazon.com/connect/latest/adminguide/contact-flow-import-export.html
5. Update the Contact flows to access Lex Chatbot CalloutBot_ExcelLexBot
6. Deploy this project.


## Deployment with AWS Serverless Application Repository
Search "awscallout" and input iInstanceId, ContactFlowId, and SourcePhoneNumber, then you can deploy it with one click!


## Build and Deployment with Cloud9
Update instanceId, contactFlowId, and sourcePhoneNumber in deployment.sh.

./setup.sh

sudo ./get_layer_packages.sh

UNIQUE_ID=change-this-to-get-a-unique-source-bucket

source deployment.sh


## How to use it without a line of code.

1. Modify contract_flow/call_job.xlsx and it is very easy to understand!
2. Upload the Excel file to ExcelCallTaskBucket.


## Sample Code to make calls

```python
import boto3
import json
import pprint
import sys

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(
    QueueName="it114115callout-CallSqsQueue-1GNVSZGI92ZYM")

test_phone_list = ["34567891", "12345678"]

task_id = "calling"
task_id = "calling2"
call_list = [{
    "id": task_id + "_" + str(i),
    "receiver_id": str(i),
    "username": "Student " + str(i),
    'phone_number': "+852" + phone_number
} for i, phone_number in enumerate(test_phone_list)]

questions = [
    {
        "question_type": "Yes/No",  # OK, Yes/No, Multiple Choice
        "question_template": "Are you using Amazon Connect?"
    },
    {
        "question_type":
        "Multiple Choice",  # OK, Yes/No, Multiple Choice
        "question_template":
        "How do you know Amazon Connect? A. News Letter, B. Social Media, C. AWS Event, D. AWS Website."
    },
    {
        "question_type": "OK",  # OK, Yes/No, Multiple Choice
        "question_template": "Do you think it is OK?"
    },
]

call_task = {
    "task_id": task_id,
    "greeting": "Hi {{ username }}, This is a simple survey.",
    "ending": "Good Bye {{ username }} and have a nice day!",
    "questions": questions,
    "receivers": call_list
}

pp = pprint.PrettyPrinter(compact=True)
pp.pprint(call_task)

print("Json Text in KB: " + str(sys.getsizeof(json.dumps(call_task)) / 1024))

response = queue.send_message(MessageBody=json.dumps(call_task))
pp.pprint(response)

```

