import os
import json


def lambda_handler(event, context):
    data = json.loads(event[0]["body"]) 
    
    return {"items":data}
