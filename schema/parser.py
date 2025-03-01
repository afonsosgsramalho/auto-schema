import json
import ast


def read_json(json_input: json) -> dict:
    with open(json_input) as f:
        dic = json.load(f)
    
    return dic


def read_input():
    pass


def read_output(output_str: str) -> dict:
    cleaned_string = output_str.replace("Output", "").strip()
    parsed_dict = ast.literal_eval(cleaned_string)
    
    return parsed_dict
