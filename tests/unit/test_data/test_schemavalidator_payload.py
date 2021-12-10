def eventbridge_payload_positive():
    ### Eventbridge payload
    return {'version': '0', 
'id': '60d01c05-c648-0ea8-3a7c-ca661d7d0560', 
'detail-type': 'xmldata', 
'source': 'custom.get_xml_lambda', 
'account': '111222333', 
'time': '2021-11-28T11:40:40Z', 
'region': 'us-east-1', 
'resources': ['string'], 
'detail': 
{'reference_id': '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-testsuccessevent', 'payloadTrimed': 'no', 'payloadS3Key': '', 
'data': '<note><to>Tove</to><from>Jani</from><heading>Reminder</heading><body>Dont forget me this weekend! er.ankit.cs@gmail.com</body></note>'
 }
}

def eventbridge_payload_negative():
    ### Eventbridge payload
    return {'version': '0', 
'id': '60d01c05-c648-0ea8-3a7c-ca661d7d0560', 
'detail-type': 'xmldata', 
'source': 'custom.get_xml_lambda', 
'account': '111222333', 
'time': '2021-11-28T11:40:40Z', 
'region': 'us-east-1', 
'resources': ['string'], 
'detail': 
{'reference_id': '57a49e9c-9803-42b4-b3e3-51f3ffab0b8a-testsuccessevent', 'payloadTrimed': 'no', 'payloadS3Key': '', 
'data': '<note><from>Jani</from><heading>Reminder</heading><body>Dont forget me this weekend! er.ankit.cs@gmail.com</body></note>'
 }
}