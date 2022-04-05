import json

print("loading function")


def respond(msg):
    return {
        "statusCode": "200",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(msg),
    }


def lambda_handler(event, context):
    return respond("Hello SAM")
