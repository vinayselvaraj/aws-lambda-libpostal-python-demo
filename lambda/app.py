import os
import json
from postal.expand import expand_address

def handler(event, context):
    result = expand_address('Quatre vingt douze Ave des Champs-Élysées')
    print(result)
    return json.dumps(result)