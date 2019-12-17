from boto3 import resource
import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import sys
sys.path.append("/opt/")
import pandas as pd

dynamodb = resource('dynamodb')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    task_id = event
    print(event)

    table = dynamodb.Table(os.environ['CallResultDynamoDBTable'])
    response = table.query(KeyConditionExpression=Key('task_id').eq(task_id))

    def convert_answer(call_record):
        call_record["answers"] = json.loads(call_record["answers"])
        for i, answer in enumerate(call_record["answers"]):
            call_record["Question " + str(i + 1)] = answer
        del call_record["answers"]
        return call_record

    df = pd.DataFrame(list(map(convert_answer, response[u'Items'])))
    filename = "/tmp/{}.xlsx".format(task_id)
    df.to_excel(filename)
    s3.upload_file(filename, os.environ['CallReportBucket'],
                   task_id + "_result.xlsx")

    excelDownloadUrl = create_presigned_url(os.environ['CallReportBucket'],
                                            task_id + "_result.xlsx")

    filename = "/tmp/{}.json".format(task_id)
    with open(filename, 'w') as json_file:
        json_file.write(df.to_json(orient='records'))
    s3.upload_file(filename, os.environ['CallReportBucket'],
                   task_id + "_result.json")

    print(df)

    return {
        "TaskId": task_id,
        "Bucket": os.environ['CallReportBucket'],
        "ExcelKey": task_id + "_result.xlsx",
        "ExcelDownloadUrl": excelDownloadUrl,
        "JsonKey": task_id + "_result.json"
    }


def create_presigned_url(bucket_name, object_name, expiration=3600 * 24 * 30):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_name
                                                    },
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    return response
