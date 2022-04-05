import json
import boto3
import os

print("loading function")
table_name = os.environ["TABLE_NAME"]
region_name = os.environ["REGION_NAME"]
dynamo = boto3.client("dynamodb", region_name=region_name)


def respond(response):
    return {
        "statusCode": "200",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }


def lambda_handler(event, context):
    result = dynamo.scan(TableName=table_name)
    return respond(result)
