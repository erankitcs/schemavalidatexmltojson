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
        apigw_event = {
        "body": '{ "reference_id": "57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-Ankit"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }
        result = lambda_handler(apigw_event,context={})
        body     = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(body["message"], "Json is Valid")
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["reference_id"], TEST_ID)