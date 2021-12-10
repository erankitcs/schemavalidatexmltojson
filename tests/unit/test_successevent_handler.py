import json
import os
import unittest
import boto3
import mock
import pytest
from moto import mock_dynamodb2
from moto import mock_s3
from botocore.exceptions import ClientError

REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'testsuccessevent-dynamodb'
TEST_ID = '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-testsuccessevent'
VALIDATION_SUCCESS_BUCKET = "testsuccessevent-success-s3-bucket"
PAYLOAD_BUCKET = "testsuccessevent-payload-s3-bucket"
@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
   

@mock_dynamodb2
@mock_s3
@mock.patch.dict(os.environ, {'DYNAMODB_TABLE': DYNAMODB_TABLE_NAME})
@mock.patch.dict(os.environ, {"REGION": REGION} )
@mock.patch.dict(os.environ, {"PAYLOAD_BUCKET": PAYLOAD_BUCKET} )
@mock.patch.dict(os.environ, {"VALIDATION_SUCCESS_BUCKET": VALIDATION_SUCCESS_BUCKET} )
class TestLambdaFunction(unittest.TestCase):

    ## Presetting up all the required AWS Resources using Moto
    def setUp(self):
        # S3 setup
        self.s3 = boto3.resource('s3', region_name=REGION)
        self.s3_success_bucket = self.s3.create_bucket(Bucket=VALIDATION_SUCCESS_BUCKET)
        self.s3_payload_bucket = self.s3.create_bucket(Bucket=PAYLOAD_BUCKET)
        # DynamoDB Setup
        self.dynamodb = boto3.resource('dynamodb')
        try: 
          self.dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            AttributeDefinitions=[{'AttributeName': 'id','AttributeType': 'S'}],
            KeySchema=[{'AttributeName': 'id','KeyType': 'HASH'}]
          )
          table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)
          table.put_item(Item={
            'id': TEST_ID,
            'status':'valid',
            'msg':  'Json is Valid',
           })
        except ClientError as e:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)

    def test_log_event(self):
        from successValidationEventProcess.app import log_event
        LOG_MSG = "Converted JSON object is saved into S3 bucket."
        LOG_STATUS = "valid and loaded"
        res = log_event(TEST_ID,LOG_STATUS,LOG_MSG)
        self.assertEqual(res, True)
        ## Getting test data from DynamoDb table.
        table = self.dynamodb.Table(DYNAMODB_TABLE_NAME)
        response = table.get_item(Key={'id': TEST_ID})
        log_record = response['Item']
        self.assertEqual(log_record["status"],LOG_STATUS )
        self.assertEqual(log_record["msg"], LOG_MSG)
    
    def test_xml_to_json(self):
        from successValidationEventProcess.app import xml_to_json
        xmldata="""<note>
        <to>Tove</to><from>Jani</from></note>
        """
        res = xml_to_json(xmldata)
        jsonRes = json.loads(res)
        self.assertEqual(jsonRes["note"]["to"],'Tove')
        self.assertEqual(jsonRes["note"]["from"],'Jani')
    def test_lambda_handler(self):
        from successValidationEventProcess.app import lambda_handler
        from tests.unit.test_data.test_successevent_payload import eventbridge_payload
        eventbridge_event = eventbridge_payload()
        result = lambda_handler(eventbridge_event,context={})
        self.assertEqual(result["statusCode"], 200)