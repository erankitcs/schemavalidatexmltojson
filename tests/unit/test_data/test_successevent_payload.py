def eventbridge_payload():
    ### Eventbridge payload
    return {'version': '0', 
'id': '60d01c05-c648-0ea8-3a7c-ca661d7d0560', 
'detail-type': 'success', 
'source': 'custom.schemavalidator_lambda', 
'account': '111222333', 
'time': '2021-11-28T11:40:40Z', 
'region': 'us-east-1', 
'resources': ['string'], 
'detail': 
{'reference_id': '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-testsuccessevent', 'payloadTrimed': 'no', 'payloadS3Key': '', 
'payload': '{"note": {"to": "Tove", "from": "Jani", "heading": "Reminder", "body": "Dont forget me this weekend! er.ankit.cs@gmail.com"}}',
'validationMsg': 'Given JSON data is Valid against Schema.',
 'isValid': True
 }
}
