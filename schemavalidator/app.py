import json
import boto3
import os
import xmltodict
import jsonschema
from jsonschema import validate

PAYLOAD_BUCKET = os.getenv('PAYLOAD_BUCKET')
REGION=os.getenv('REGION')

s3 = boto3.resource('s3', region_name=REGION)

def xml_to_json(xmldata):
    xpars = xmltodict.parse(xmldata)
    jsonData = json.dumps(xpars)
    print('json data')
    print(jsonData)
    return jsonData
def get_payload(key):
    s3_object = s3.Object(bucket_name=PAYLOAD_BUCKET, key=key)
    xmlpayload = s3_object.get()['Body'].read()
    return xmlpayload

def get_schema():
    # This function loads the given schema available
    with open('Schema.json', 'r') as file:
        schema = json.load(file)
    return schema
def validate_json(json_data):
    ## Getting Schema to validate
    schema = get_schema()
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message
def lambda_handler(event, context):
    """Lambda function to validate passed XML data and do json schema validation from Event Bridge..

    Parameters
    ----------
    event: dict, required
        Eventbridge schema object.
    context: object, required
        Lambda Context runtime methods and attributes
    Returns
    ------
    Processing status Output Format: json
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
    payload=detail["data"]
    jsonpayload=xml_to_json(payload)
    isValid , msg = validate_json(jsonpayload)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": msg,
            "reference_id": reference_id,
            "isValid": isValid
        }),
    }
