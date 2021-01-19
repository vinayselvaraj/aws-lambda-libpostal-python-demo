import os
import json
from postal.parser import parse_address
from postal.expand import expand_address

def handler(event, context):

    expanded_addresses = expand_address(event['address'])

    results = []

    for expanded_address in expanded_addresses:
      parse_output = parse_address(expanded_address)
      result = dict()
      for i in parse_output:
        result[i[1]] = i[0]
      results.append(result)
    
    return result