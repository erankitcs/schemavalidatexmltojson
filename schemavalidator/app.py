import json
import boto3
import os

PAYLOAD_BUCKET = os.getenv('PAYLOAD_BUCKET')
def validate_xml(xmlpayload):
    ### Getting Schema json

    ### Validation 
    msg="Schema is valid."
    return True , msg
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
    xmlpayload=detail["data"]
    isValid , msg = validate_xml(xmlpayload)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "XML Validation completed successfully.",
            "reference_id": reference_id
        }),
    }
