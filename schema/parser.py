import json
import os
import ast
import logging


def create_json_file(file_path:str, target_file:str, tables_fields:list):
    json_string = json.dumps(tables_fields, indent=4)

    with open(f'{file_path}/{target_file}', 'w') as json_file:
        json_file.write(json_string)

    print(f'Json of fields have been written to {file_path}')


def create_sql_file(file_path:str, target_file:str, query_list:list):
    query_number = 1
    with open(f'{file_path}/{target_file}', 'w') as file:
        for sql_query in query_list:
            file.write(f'-- Query number {query_number}\n')
            file.write(f'{sql_query};\n\n')
            query_number += 1

    print(f'SQL queries have been written to {file_path}')
    

def create_csv_file(file_path:str, target_file:str, df):
    df.write_csv(f'{file_path}/{target_file}', separator=',')

    print(f'CSV file has been written to {file_path}')


def read_json(json_input:json) -> dict:
    with open(json_input) as f:
        dic = json.load(f)
    
    return dic


def read_output(output_str:str) -> dict:
    cleaned_string = output_str.replace("Output", "").strip()
    parsed_dict = ast.literal_eval(cleaned_string)
    
    return parsed_dict
