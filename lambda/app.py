import os
import json
from postal.parser import parse_address

def handler(event, context):
    parse_output = parse_address(event['address'])
    result = dict()
    for i in parse_output:
      output[i[1]] = i[0]
    return json.dumps(result)