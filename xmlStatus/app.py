import json
import boto3
from boto3.dynamodb.conditions import Key
import os

DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
REGION=os.getenv('REGION')

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table(DYNAMODB_TABLE)
def check_status(id):
    response = table.query(
        KeyConditionExpression=Key('id').eq(id)
    )
    status = response['Items'][0]["status"]
    msg    = response['Items'][0]["msg"]
    return msg,status

def lambda_handler(event, context):
    """Lambda function to check status of xml schema validation and json conversion request.

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes
    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    print(event)
    body = json.loads(event["body"])
    reference_id   = body["reference_id"]
    msg,status=check_status(reference_id)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": msg,
            "status": status,
            "reference_id": reference_id
        }),
    }
