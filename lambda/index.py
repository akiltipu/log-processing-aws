import json
import base64
import re

def redact_sensitive_info(data_str):
    # Regex patterns for password and API key
    patterns = [
        (r'"password"\s*:\s*"[^"]*"', '"password":"********"'),
        (r'"api_key"\s*:\s*"[^"]*"', '"api_key":"********"')
    ]
    
    for pattern, replacement in patterns:
        data_str = re.sub(pattern, replacement, data_str)
    
    return data_str

def lambda_handler(event, context):
    output_records = []

    for record in event['records']:
        # Decode the record data
        payload = base64.b64decode(record['data']).decode('utf-8')

        # Redact sensitive information using regex
        redacted_payload = redact_sensitive_info(payload)

        # Encode the redacted data back to base64
        encoded_payload = base64.b64encode(redacted_payload.encode('utf-8')).decode('utf-8')

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': encoded_payload
        }
        output_records.append(output_record)

    return {'records': output_records}
