from ast import literal_eval
import json

def str_to_valid_dict(input: str, place:str = "") -> dict | None:
    if not input:
        return None
    
    error_msg = f"Invalid dictionary format. {place}"
    
    try:
        output_dict = literal_eval(input)
    except:
        raise Exception(error_msg)
    
    if type(output_dict) != type(dict()):
        raise Exception(error_msg)
    
    # for key, value in output_dict.items():
    #     if type(key) != type(str()):
    #         raise Exception(error_msg)
    #     if type(value) != type(str()):
    #         raise Exception(error_msg)

    return output_dict

def valid_json_to_py_object(input: str):
    if not input:
        return None
    
    try:
        output = json.loads(input)
    except Exception as e:
        raise e
    
    return output
    