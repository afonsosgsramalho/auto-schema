# Deal with the creation of files for the upload and the management of them in the local disk
import os
import polars as pl
import json
import io
import ast
import logging
import pendulum


class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._create_files_folder()


    def _create_files_folder(self, path=None):
        # Determine the full path to create
        if path:
            full_path = os.path.join(self.file_path, path)
        else:
            full_path = self.file_path

        # Create the directory if it doesn't exist
        try:
            os.makedirs(full_path, exist_ok=True)
            print(f'Folder created or already exists at {full_path}')
        except Exception as e:
            print(f'Error creating folder: {e}')
            raise


    def create_json_file(self, path: str, target_file: str, tables_fields: list):
        self._create_files_folder(path)
        json_string = json.dumps(tables_fields, indent=4)

        try:
            file_path = os.path.join(self.file_path, path, target_file)
            with open(file_path, 'w') as json_file:
                json_file.write(json_string)
            print(f'JSON of fields has been written to {file_path}')
        except Exception as e:
            print(f'Error writing JSON file: {e}')
            raise


    def create_text_file(self, path:str, target_file:str, query_list:list):
        self._create_files_folder(path)

        try:
            query_number = 1
            with open(f'{self.file_path}/{path}/{target_file}', 'w') as file:
                for sql_query in query_list:
                    file.write(f'-- Query number {query_number}\n')
                    file.write(f'{sql_query};\n\n')
                    query_number += 1
            print(f'SQL queries have been written to {self.file_path}/{path}/{target_file}')
        except Exception as e:
            print(f'Error writing text file: {e}')
            raise


    def create_csv_file(self, path:str, target_file:str, df:pl.DataFrame):
        self._create_files_folder(path)

        try:
            df.write_csv(f'{self.file_path}/{path}/{target_file}', separator=',')
            print(f'CSV file has been written to {self.file_path}/{path}/{target_file}')
        except Exception as e:
            print(f'Error writing Csv file: {e}')
            raise

    
    def create_javascript_file(self, path:str, target_file:str)


class FileReader:
    def __init__(self):
        pass

    def validate(self):
        pass


    def read_json(self, json_input:json) -> dict:
        with open(json_input) as f:
            dic = json.load(f)
    
        return dic


    def read_output(self, output_str:str) -> dict:
        cleaned_string = output_str.replace("Output", "").strip()
        parsed_dict = ast.literal_eval(cleaned_string)
        
        return parsed_dict
    

    def dataframe_to_prompt(self, df:pl.DataFrame, format:str = 'csv', limit:int = 10) -> str:
        if limit is not None:
            df = df.head(limit)

        if format == 'csv':
            output = io.StringIO()
            df.write_csv(output, include_header=True)
            return output.getvalue()
        elif format == 'json':
            json_list = df.to_dicts()
            json_string = json.dumps(json_list, ident=4)
            return json_string
        else:
            raise ValueError('Format must be "csv" or "json"')
