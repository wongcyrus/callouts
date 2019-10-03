import os
import datetime
import json
import sys
sys.path.append("/opt/")
import boto3

stepfunctions_client = boto3.client("stepfunctions")


def lambda_handler(event, context):
    print(event)

    taskToken = event["Details"]["ContactData"]["Attributes"]["taskToken"]
    message = event["Details"]["ContactData"]["Attributes"]
    del message["taskToken"]
    del message["response_hanlder_function_arn"]

    message["response_intent"] = event["Details"]["Parameters"][
        "response_intent"]

    stepfunctions_client.send_task_success(taskToken=taskToken,
                                           output=json.dumps(message))
    return event
