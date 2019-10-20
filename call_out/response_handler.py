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
    message["response_intent"] = event["Details"]["Parameters"][
        "response_intent"]
    message["error"] = "null"

    if "intent_answer" in message and message["intent_answer"] is not "":
        message["answer"] = message["intent_answer"]
        answer = message["intent_answer"]
    else:
        answer = message["response_intent"].replace("CalloutBot_",
                                                    "").replace("Intent", "")
        message["answer"] = answer

    message["intent_answer"] = ""

    previous_answer = json.loads(message["answers"])
    previous_answer.append(answer)
    message["answers"] = json.dumps(previous_answer)

    return message
