import json
import boto3
import os

OBJECTLAMBDAS3ARN = os.getenv('OBJECTLAMBDAS3ARN')
REGION=os.getenv('REGION')

s3 = boto3.client('s3')

def get_json(objKey):
    """
    Get JSON Object from S3.
    """
    s3data = s3.get_object(Bucket=OBJECTLAMBDAS3ARN,Key=objKey)
    s3redacteddata = s3data['Body']
    jsonData = json.load(s3redacteddata)
    return jsonData, "success"
def lambda_handler(event, context):
    """Lambda function to read S3 Json via Object Lambda Access Point.

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
    data,status=get_json(reference_id)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": data,
            "reference_id": reference_id,
            "status": status
        }),
    }
