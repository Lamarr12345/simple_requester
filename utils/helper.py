import json

def valid_json_to_py_object(input: str):
    if not input:
        return None
    
    try:
        output = json.loads(input)
    except Exception as e:
        raise e
    
    return output