import json
import os
import unittest
import boto3
import mock
import pytest
from moto import mock_dynamodb2
from botocore.exceptions import ClientError

REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'testxmlstatus-dynamodb'
TEST_ID = '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-Ankit'

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
   

@mock_dynamodb2
@mock.patch.dict(os.environ, {'DYNAMODB_TABLE': DYNAMODB_TABLE_NAME})
@mock.patch.dict(os.environ, {"REGION": REGION} )
class TestLambdaFunction(unittest.TestCase):

    ## Presetting up all the required AWS Resources using Moto
    def setUp(self):
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
            'status':'success',
            'msg':  'Json is Valid',
           })
        except ClientError as e:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)

    def test_check_status(self):
        from xmlStatus.app import check_status
        msg,status = check_status(TEST_ID)
        self.assertEqual(msg, "Json is Valid")
        self.assertEqual(status, "success")

    def test_lambda_handler(self):
        from xmlStatus.app import lambda_handler
        from tests.unit.test_data.test_xmlstatus_payload import apigw_xmlstatuspayload_event
        apigw_event = apigw_xmlstatuspayload_event()
        result = lambda_handler(apigw_event,context={})
        body     = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(body["message"], "Json is Valid")
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["reference_id"], TEST_ID)