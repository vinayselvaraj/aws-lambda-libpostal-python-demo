import os
import json
from postal.expand import expand_address
from postal.parser import parse_address

def handler(event, context):
    result = parse_address(event['address'])
    print(result)
    return json.dumps(result)