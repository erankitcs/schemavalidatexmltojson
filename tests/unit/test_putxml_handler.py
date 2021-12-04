import json
import os
import unittest
import boto3
import mock
import pytest
from moto import mock_dynamodb2
from moto import mock_s3
from moto import mock_events
from botocore.exceptions import ClientError
from datetime import datetime

REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'testputxml-dynamodb'
TEST_ID = '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-testputxml'
S3_BUCKET_NAME = 'testputxml-s3-bucket'
EVENTBRIDGE_NAME = 'testputxml-eventbridge'
@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@mock_dynamodb2
@mock_s3
@mock_events
@mock.patch.dict(os.environ, {'DYNAMODB_TABLE': DYNAMODB_TABLE_NAME})
@mock.patch.dict(os.environ, {'PAYLOAD_BUCKET': S3_BUCKET_NAME})
@mock.patch.dict(os.environ, {"REGION": REGION} )
@mock.patch.dict(os.environ, {"EVENTBRIDGE": EVENTBRIDGE_NAME} )
class TestPutXmlLambdaFunction(unittest.TestCase):
    ## Presetting up all the required AWS Resources using Moto
    def setUp(self):
      
        # S3 setup
        self.s3 = boto3.resource('s3', region_name=REGION)
        self.s3_bucket = self.s3.create_bucket(Bucket=S3_BUCKET_NAME)
        ## DynamoDb 
        self.dynamodb = boto3.resource('dynamodb')
        try: 
          self.dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}]
          )
        except ClientError as e:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)
        ## Setup Event Bridge
        self.events_client = boto3.client('events')
        try:
            self.event_name = self.events_client.create_event_bus(
                          Name=EVENTBRIDGE_NAME,
                         )
        except ClientError as e:
            self.event_name = self.events_client.describe_event_bus(Name=EVENTBRIDGE_NAME)



    def test_log_event(self):
        from putXml.app import log_event
        STATUS = "recieved"
        MSG="Items has been recieved for processing."
        res = log_event(TEST_ID,STATUS,MSG)
        self.assertEqual(res, True)
        table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)
        response = table.get_item(Key={'id': TEST_ID})
        log_record = response['Item']
        self.assertEqual(log_record["status"], STATUS)
        self.assertEqual(log_record["msg"], MSG)
    
    def test_upload_payload(self):
        from putXml.app import upload_payload
        PAYLOAD="Items has been recieved for processing."
        res = upload_payload(PAYLOAD,TEST_ID)
        self.assertEqual(res, True)
        obj = self.s3.Object(bucket_name=S3_BUCKET_NAME, key=TEST_ID)
        response = obj.get()
        data = response['Body'].read().decode("utf-8") 
        self.assertEqual(str(data), PAYLOAD)
    
    def test_lambda_handler_smallpayload(self):
        from putXml.app import lambda_handler
        from tests.unit.test_data.test_putxml_small_payload import apigw_smallpayload_event
        apigw_event = apigw_smallpayload_event()
        result = lambda_handler(apigw_event,context={})
        body   = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(body["message"], "XML is submitted for schema validation and further json conversion.")
        reference_id = body["reference_id"]
        print(reference_id)

    def test_lambda_handler_largepayload(self):
        from putXml.app import lambda_handler
        from tests.unit.test_data.test_putxml_large_payload import apigw_largepayload_event
        apigw_event = apigw_largepayload_event()
        result = lambda_handler(apigw_event,context={})
        body   = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(body["message"], "XML is submitted for schema validation and further json conversion.")
        reference_id = body["reference_id"]
        now = datetime.now()
        today = str(now)[:14]
        objKey=today+"/"+reference_id
        objs = list(self.s3_bucket.objects.filter(Prefix=objKey))
        print(objs)
        self.assertEqual(objKey, objs[0].key)