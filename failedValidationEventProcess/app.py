import json
import boto3
import os

FAILED_BUCKET = os.getenv('VALIDATION_FAILED_BUCKET')
PAYLOAD_BUCKET = os.getenv('PAYLOAD_BUCKET')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
REGION=os.getenv('REGION')

s3 = boto3.resource('s3', region_name=REGION)

def upload_s3(data,key):
    bucket = s3.Bucket(FAILED_BUCKET)
    response = bucket.put_object(Body=data,Key=key)
    print(response)
    return True

def lambda_handler(event, context):
    """Lambda function to recieved Failed Json payload and upload it to S3 bucket.

    Parameters
    ----------
    event: dict, required
        AWS Lambda invoke from SQS.
    context: object, required
        Lambda Context runtime methods and attributes
    Returns
    ------
    Upload Status Output Format: json
    """
    print(event)
    detail = json.loads(event["detail"])
    print(detail)
    reference_id=detail["reference_id"]
    data=detail["data"]
    upload_s3(data,reference_id)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Json Object loaded to S3 successfully.",
            "reference_id": reference_id
        }),
    }
