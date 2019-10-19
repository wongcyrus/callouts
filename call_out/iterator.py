import os
import datetime
import json
import sys
sys.path.append("/opt/")
import boto3

stepfunctions_client = boto3.client("stepfunctions")


def lambda_handler(event, context):
    print(event)
    data = event["Details"]["ContactData"]["Attributes"]
    questions = json.loads(data["questions"])
    question = questions[int(data["i"])]
    data["question"] = question["question"]
    data["question_type"] = question["question_type"]
    data["i"] = int(data["i"]) + 1
    data["question_id"] = str(data["id"]) + "_q" + str(data["i"])
    print(data)
    return data
