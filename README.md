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
import pprint
import sys

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(
    QueueName="it114115callout-CallSqsQueue-1GNVSZGI92ZYM")

test_phone_list = ["34567891", "12345678"]

task_id = "calling"
call_list = [{
    "id": task_id + "_" + str(i),
    "username": "Student " + str(i),
    'phone_number': "+852" + phone_number
} for i, phone_number in enumerate(test_phone_list)]

questions = [
    {
        "question_type": "Yes/No",  # OK, Yes/No, Multiple Choice
        "question_template": "Hi {{ username }}, test 1!"
    },
    {
        "question_type": "Multiple Choice",  # OK, Yes/No, Multiple Choice
        "question_template": "Answer the letter now shown in project!"
    }
]

call_task = {
    "task_id": task_id,
    "questions": questions,
    "receivers": call_list
}

pp = pprint.PrettyPrinter(compact=True)
pp.pprint(call_task)

print("Json Text in KB: " + str(sys.getsizeof(json.dumps(call_task)) / 1024))

response = queue.send_message(MessageBody=json.dumps(call_task))
pp.pprint(response)

```

