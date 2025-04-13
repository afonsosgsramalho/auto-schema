from typing import Optional, List, Dict
import os
import polars as pl
import json
import io
import ast

from sources.aws import AWSClientManager
from exceptions import FileExtractionError

class FileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._create_files_folder()


    def _create_files_folder(self, path:Optional[str]=None):
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


    def create_json_file(self, path:str, target_file:str, tables_fields:Dict[str, str]):
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


    def create_text_file(self, path:str, target_file:str, query_list:List[str]):
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
        csv_files_path = f'{path}/csv_files'
        self._create_files_folder(csv_files_path)

        try:
            df.write_csv(f'{self.file_path}/{csv_files_path}/{target_file}', separator=',')
            print(f'CSV file has been written to {self.file_path}/{path}/{target_file}')
        except Exception as e:
            print(f'Error writing Csv file: {e}')
            raise


class FileReader:
    def read_json(self, json_input:json):
        with open(json_input) as f:
            dic = json.load(f)
    
        return dic


    def read_output(self, output_str:str):
        cleaned_string = output_str.replace("Output", "").strip()
        parsed_dict = ast.literal_eval(cleaned_string)
        
        return parsed_dict
    

    def dataframe_to_prompt(self, df:pl.DataFrame, format:Optional[str]='csv', limit:Optional[int]=10):
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
            raise ValueError('Format must be CSV or JSON')


class FileExtractor:
    def __init__(
        self,
        aws_client: AWSClientManager,
        file_manager: FileManager,
        bucket_output: str,
    ):
        self.aws_client = aws_client
        self.file_manager = file_manager
        self.bucket_output = bucket_output
        self.file_reader = FileReader()


    def extract_table_schemas(self, database:str):
        try:
            tables = self.aws_client.get_glue_tables(database)
            tables_fields = {}

            for table in tables:
                tables_fields[table] = self.aws_client.get_table('silver', table)

            return tables_fields
        except Exception as e:
            raise FileExtractionError(f"Failed to extract SQL queries: {e}") from e


    def extract_sql_queries(self):
        try:
            return self.aws_client.get_all_query_strings()
        except Exception as e:
            raise FileExtractionError(f"Failed to extract SQL queries: {e}") from e


    def extract_data_samples(self, database:str, path:str):
        tables_data = []

        try:
            tables = self.aws_client.get_glue_tables(database)

            for table in tables:
                query_data = self.aws_client.get_query_data(database, table, self.bucket_output)
                table_data = self.file_reader.dataframe_to_prompt(query_data)
                tables_data.append(table_data)
                self.file_manager.create_csv_file(path, f"{table}.csv", query_data)
            return tables_data

        except Exception as e:
            raise FileExtractionError(f"Failed to extract data samples: {e}")