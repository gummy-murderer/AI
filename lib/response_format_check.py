import json


def response_format(answer):
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None