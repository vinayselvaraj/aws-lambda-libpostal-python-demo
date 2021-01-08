import os
import json
from postal.expand import expand_address

def handler(event, context):
    result = expand_address(event['address'])
    print(result)
    return json.dumps(result)