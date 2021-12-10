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
from unittest.mock import patch, mock_open

from tests.unit.test_data.test_schemavalidator_payload import eventbridge_payload_negative, eventbridge_payload_positive

REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'schemavalidator-dynamodb'
TEST_ID = '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-schemavalidator'
EVENTBRIDGE = "schemavalidator-eventbridge"
PAYLOAD_BUCKET = "schemavalidator-payload-s3-bucket"
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
@mock.patch.dict(os.environ, {"REGION": REGION} )
@mock.patch.dict(os.environ, {"PAYLOAD_BUCKET": PAYLOAD_BUCKET} )
@mock.patch.dict(os.environ, {"EVENTBRIDGE": EVENTBRIDGE} )
class TestLambdaFunction(unittest.TestCase):

    ## Presetting up all the required AWS Resources using Moto
    def setUp(self):
        # S3 setup
        self.s3 = boto3.resource('s3', region_name=REGION)
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
            'status':'recieved',
            'msg':  'XML Recieved',
           })
        except ClientError as e:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)
        ## Setup Event Bridge
        self.events_client = boto3.client('events')
        try:
            self.event_name = self.events_client.create_event_bus(
                          Name=EVENTBRIDGE,
                         )
        except ClientError as e:
            self.event_name = self.events_client.describe_event_bus(Name=EVENTBRIDGE)

    def test_validate_json_positive(self):
        from schemavalidator.app import validate_json
        json_data = json.dumps({"note": {"to": "Tove","from": "Jani", "heading": "Reminder", "body": "Dont forget me this weekend! er.ankit.cs@gmail.com"}})
        schema = json.dumps({
	"$schema":"http://json-schema.org/draft-04/schema#",
	"title": "note",
	"description": "A Note request json",
	"type": "object",
    "additionalProperties": False,
	"properties": {
		"note": {
			"type": "object",
			"properties": {
				"to": {
					"description": " Sending to",
					"type": "string"
				},
				"from": {
					"description": " Sender ",
					"type": "string"
				},
				"heading": {
					"description": " Subject ",
					"type": "string"
				},
				"body": {
					"description": " Body ",
					"type": "string"
				}
			},
			"required": ["to", "from"]

		}
	},
	"required": ["note"]
})
        open_mock = mock_open(read_data=schema)
        with patch("schemavalidator.app.open", open_mock, create=True):
             status, msg = validate_json(json_data)
        open_mock.assert_called_with("Schema.json", "r")
        self.assertEqual(status, True)
    
    def test_validate_json_negative(self):
        from schemavalidator.app import validate_json
        json_data = json.dumps({"note": {"from": "Jani", "heading": "Reminder", "body": "Dont forget me this weekend! er.ankit.cs@gmail.com"}})
        schema = json.dumps({
	"$schema":"http://json-schema.org/draft-04/schema#",
	"title": "note",
	"description": "A Note request json",
	"type": "object",
    "additionalProperties": False,
	"properties": {
		"note": {
			"type": "object",
			"properties": {
				"to": {
					"description": " Sending to",
					"type": "string"
				},
				"from": {
					"description": " Sender ",
					"type": "string"
				},
				"heading": {
					"description": " Subject ",
					"type": "string"
				},
				"body": {
					"description": " Body ",
					"type": "string"
				}
			},
			"required": ["to", "from"]

		}
	},
	"required": ["note"]
})
        open_mock = mock_open(read_data=schema)
        with patch("schemavalidator.app.open", open_mock, create=True):
             status, msg = validate_json(json_data)
        open_mock.assert_called_with("Schema.json", "r")
        self.assertEqual(status, False)
    
    def test_lambda_handler(self):
        from schemavalidator.app import lambda_handler
        from tests.unit.test_data.test_schemavalidator_payload import eventbridge_payload_positive
        from tests.unit.test_data.test_schemavalidator_payload import eventbridge_payload_negative
        schema = json.dumps({
	"$schema":"http://json-schema.org/draft-04/schema#",
	"title": "note",
	"description": "A Note request json",
	"type": "object",
    "additionalProperties": False,
	"properties": {
		"note": {
			"type": "object",
			"properties": {
				"to": {
					"description": " Sending to",
					"type": "string"
				},
				"from": {
					"description": " Sender ",
					"type": "string"
				},
				"heading": {
					"description": " Subject ",
					"type": "string"
				},
				"body": {
					"description": " Body ",
					"type": "string"
				}
			},
			"required": ["to", "from"]

		}
	},
	"required": ["note"]
}) 
        open_mock = mock_open(read_data=schema)
        event = eventbridge_payload_positive()
        with patch("schemavalidator.app.open", open_mock, create=True):
             res = lambda_handler(event,context={})
             print(res)
             jsonBody = json.loads(res["body"])
        open_mock.assert_called_with("Schema.json", "r")
        self.assertEqual(res["statusCode"], 200)
        self.assertEqual(jsonBody["isValid"], True)
        event = eventbridge_payload_negative()
        with patch("schemavalidator.app.open", open_mock, create=True):
             res = lambda_handler(event,context={})
             jsonBody = json.loads(res["body"])
        self.assertEqual(res["statusCode"], 200)
        self.assertEqual(jsonBody["isValid"], False)