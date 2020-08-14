import json

def jcopy(object):
    return json.loads(json.dumps(object))
