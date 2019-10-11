import boto3
import os
import sys
import json
sys.path.append("/opt/")
from urllib.parse import unquote_plus
import pandas as pd
from pandas.api.types import is_numeric_dtype

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        download_path = '/tmp/{}'.format(key)

        s3.download_file(bucket, key, download_path)

        task_id = key.replace(".xlsx", "")
        excel_file = download_path
        configures = pd.read_excel(
            excel_file,
            sheet_name="configures",
        ).fillna('').to_dict()

        questions = pd.read_excel(
            excel_file, sheet_name="questions").dropna().to_dict('records')

        receivers = pd.read_excel(excel_file, sheet_name="receivers")
        receivers = receivers.dropna()
        receivers.rename(columns={'id': 'receiver_id'}, inplace=True)
        if is_numeric_dtype(receivers['receiver_id']):
            receivers.receiver_id = receivers.receiver_id.apply(
                lambda x: str(int(x)))

        receivers["id"] = list(
            map(lambda x: task_id + "_" + str(x), receivers["receiver_id"]))

        receivers["phone_number"] = list(
            map(
                lambda x: "+" + str(configures["phone_prefix"][0]) + str(int(
                    x)), receivers["phone_number"]))

        receivers = receivers.to_dict('records')

        print(configures)
        print(questions)
        print(receivers)

        call_task = {
            "task_id": task_id,
            "greeting": configures["greeting"][0],
            "ending": configures["ending"][0],
            "questions": questions,
            "receivers": receivers
        }
        print(call_task)

        print("Json Text in KB: " +
              str(sys.getsizeof(json.dumps(call_task)) / 1024))

        response = sqs.send_message(QueueUrl=os.environ['CallSqsQueueUrl'],
                                    MessageBody=json.dumps(call_task))
        print(response)
        return response
