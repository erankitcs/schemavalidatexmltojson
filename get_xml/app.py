import json
import sys
import uuid
import os
import boto3
from datetime import datetime

PAYLOAD_BUCKET = os.getenv('PAYLOAD_BUCKET')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
EVENTBRIDGE = os.getenv('EVENTBRIDGE')
REGION=os.getenv('REGION')

s3 = boto3.resource('s3', region_name=REGION)
events_client = boto3.client('events')

def upload_payload(payload,objkey):
    """
    This function will uplaod payload to S3 bucket.
    
    """
    bucket = s3.Bucket(PAYLOAD_BUCKET)
    response = bucket.put_object(Body=payload,Key=objkey)
    print(response)
    return True

def lambda_handler(event, context):
    """Lambda function to check xml payload size and route request to EventBridge.

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
    client   = body["metadata"]["client"]
    payload  = body["data"]
    uniqueid = str(uuid.uuid4())
    reference_id = uniqueid+"-"+client
    print("checking payload size coming from the request.")
    payload_size = sys.getsizeof(payload)/1024
    if payload_size > 250 :
        print("Payload is too large for Eventbridge. Payload size- ", payload_size)
        now = datetime.now()
        today = str(now)[:14]
        objKey=today+"/"+reference_id
        upload_payload(payload,objKey)
        body["data"] = ""
        body["payloadTrimed"]="yes"
        body["payloadS3Key"]=objKey
    else:
        print("Good to go for eventbridge directly. Payload size- ", payload_size)
        body["payloadTrimed"]="no"
    print("Calling Event Bridge with request payload.")
    ### Adding Reference into payload.
    body["reference_id"]=reference_id
    Entries=[
        {
            'Time': datetime.now(),
            'Source': 'custom.get_xml_lambda',
            'Resources': [
                'string',
            ],
            'DetailType': 'xmldata',
            'Detail': json.dumps(
                body
            ),
            'EventBusName': EVENTBRIDGE,
            'TraceHeader': reference_id
        },
    ]
    print(Entries)
    response = events_client.put_events(
    Entries=Entries
     )
    print(response)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "XML is submitted for schema validation and further json conversion.",
            "reference_id": reference_id
        }),
    }
