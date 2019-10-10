from boto3 import resource
import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key

import sys
sys.path.append("/opt/")
import pandas as pd

dynamodb = resource('dynamodb')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    task_id = event
    print(event)

    table = dynamodb.Table(os.environ['CallResultDynamoDBTable'])
    response = table.query(
        ProjectionExpression=
        "task_id, receiver_id, answers, call_at, #st, #err, username",
        ExpressionAttributeNames={
            "#st": "status",
            "#err": "error"
        },
        KeyConditionExpression=Key('task_id').eq(task_id))

    def convert_answer(call_record):
        call_record["answers"] = json.loads(call_record["answers"])
        for i, answer in enumerate(call_record["answers"]):
            call_record["Question " + str(i + 1)] = answer
        del call_record["answers"]
        return call_record

    df = pd.DataFrame(list(map(convert_answer, response[u'Items'])))
    filename = "/tmp/{}.xlsx".format(task_id)
    df.to_excel(filename)

    s3.upload_file(filename, os.environ['ExcelCallResultBucket'],
                   task_id + "_result.xlsx")
    print(df)

    return "Finish"
