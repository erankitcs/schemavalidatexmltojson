import json
import boto3
import os
import xmltodict

SUCCESS_BUCKET = os.getenv('VALIDATION_SUCCESS_BUCKET')
PAYLOAD_BUCKET = os.getenv('PAYLOAD_BUCKET')
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
REGION=os.getenv('REGION')

s3 = boto3.resource('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb')
def log_event(id,msg):
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.update_item(
        Key={'id': id},
        AttributeUpdates={
        'msg': msg
        },
    )
    return True
def upload_s3(data,key):
    bucket = s3.Bucket(SUCCESS_BUCKET)
    response = bucket.put_object(Body=data,Key=key)
    print(response)
    return True
def get_payload(key):
    s3_object = s3.Object(bucket_name=PAYLOAD_BUCKET, key=key)
    xmlpayload = s3_object.get()['Body'].read()
    return xmlpayload

def xml_to_json(xmldata):
    xpars = xmltodict.parse(xmldata)
    jsonData = json.dumps(xpars)
    print('json data')
    print(jsonData)
    return jsonData

def lambda_handler(event, context):
    """Lambda function to recieved Json payload and upload it to S3 bucket.

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
    print("checking if payload data is in S3 bucket or in the request.")
    if detail["payloadTrimed"] == "yes":
        payloads3key=detail["payloadS3Key"]
        print(payloads3key)
        payload = get_payload(payloads3key)
        jsonpayload=xml_to_json(payload)
    else:
        jsonpayload=detail["payload"]
    jsonpayload["valid"]=detail["isValid"]
    upload_s3(jsonpayload,reference_id)
    log_event(reference_id,"Converted a valid JSON object is saved into S3 bucket.")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Json Object loaded to S3 successfully.",
            "reference_id": reference_id
        }),
    }
