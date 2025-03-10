import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
import time
import polars as pl
from dotenv import load_dotenv
load_dotenv()


class AWSClientManager:
    def __init__(self):
        self.REGION_NAME = os.getenv('AWS_REGION')
        self.ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        self.SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    def create_client(self, service: str):
        client = boto3.client(
            service_name=service,
            region_name=self.REGION_NAME,
            aws_access_key_id=self.ACCESS_KEY_ID,
            aws_secret_access_key=self.SECRET_ACCESS_KEY
        )
        return client

    # Glue functions
    def get_table(self, database_name: str, table_name: str):
        glue_client = self.create_client('glue')
        try:
            response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
            fields = []
            for param in response.get('Table').get('StorageDescriptor').get('Columns'):
                col_name = param.get('Name')
                col_type = param.get('Type')
                fields.append((col_name, col_type))
            return fields
        except ClientError as e:
            if e.response["Error"]["Code"] == "EntityNotFoundException":
                return False

    def get_databases(self):
        glue_client = self.create_client('glue')
        try:
            response = glue_client.get_databases()
            databases = [database.get('Name') for database in response.get('DatabaseList')]
        except glue_client.exceptions.EntityNotFoundException:
            print('We cannot query databases right now')
        return databases

    def get_glue_tables(self, database_name: str):
        glue_client = self.create_client('glue')
        try:
            tables = []
            response = glue_client.get_tables(DatabaseName=database_name)
            for table in response.get('TableList', []):
                tables.append(table['Name'])
        except glue_client.exceptions.EntityNotFoundException:
            print(f"Database '{database_name}' not found.")
        return tables

    # Athena functions
    def get_all_query_strings(self):
        athena_client = self.create_client('athena')
        query_strings = []
        next_token = None
        try:
            while True:
                if next_token:
                    response = athena_client.list_query_executions(NextToken=next_token)
                else:
                    response = athena_client.list_query_executions()
                query_execution_ids = response.get('QueryExecutionIds')
                for query_execution_id in query_execution_ids:
                    query_details = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
                    query_string = query_details['QueryExecution']['Query'].strip('\n').strip()
                    query_result = query_details['QueryExecution']['Status']['State']
                    if query_result == 'SUCCEEDED' and ('join' in query_string or 'JOIN' in query_string):
                        query_strings.append(query_string)
                        break
                next_token = response.get('NextToken', None)
                if not next_token:
                    break
        except athena_client.exceptions.InvalidRequestException:
            print(f'Athena queries are not available at this moment')
        return query_strings

    def _get_query_execution(self, database_name: str, table_name: str, output_location: str, limit=None):
        athena_client = self.create_client('athena')
        query = f'SELECT * FROM {database_name}.{table_name}'

        if limit is not None:
            query += f' LIMIT {limit}'

        # Start query execution
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database_name},
            ResultConfiguration={'OutputLocation': output_location}
        )

        query_execution_id = response['QueryExecutionId']

        return query_execution_id
                
    def _wait_execution(self, query_execution_id: int):
        athena_client = self.create_client('athena')
        state = 'RUNNING'
        
        while state in ['RUNNING', 'QUEUED']:
            response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            state = response['QueryExecution']['Status']['State']
            
            if state in ['FAILED', 'CANCELLED']:
                raise Exception(f"Query failed or was cancelled: {response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')}")
            time.sleep(1)

        results_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)

        return results_response
    
    def get_query_data(self, database_name:str, table_name:str, output_location:str, limit=None):
        query_execution_id = self._get_query_execution(database_name, table_name, output_location, limit)
        response = self._wait_execution(query_execution_id)

        result_data = response['ResultSet']['Rows']
        columns = [col['VarCharValue'] for col in result_data[0]['Data']]
        rows = [[col.get('VarCharValue', '') for col in row['Data']] for row in result_data[1:]]
        
        # Create a Polars DataFrame
        df = pl.DataFrame(rows, schema=columns, orient='row')

        return df
