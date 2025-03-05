import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

REGION_NAME = os.getenv('AWS_REGION')
ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCES_KEY')

class AWS:
    def __init__(self, region_name, access_key_id, secret_access_key):
        self.region_name = region_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def _create_client(self, service:str):
        client = boto3.client(
            service_name=service,
            region_name=self.region_name,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )

        return client



# Clients
def create_client(service: str):
    client = boto3.client(
        service_name=service,
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )

    return client


# S3 functions
def s3_object_exists(bucket_name: str, object_key: str):
    s3_client = create_client('s3')
    
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Object {object_key} does not exist.")
            return False
        else:
            print(f"An error occurred: {e}") 


# Glue functions  
def check_table_exists(database_name: str, table_name: str):
    glue_client = create_client('glue')

    try:
        response = glue_client.get_table(DatabaseName=database_name, Name=table_name)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityNotFoundException":
            return False
        

def get_table(database_name: str, table_name: str):
    glue_client = create_client('glue')

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


def get_databases():
    glue_client = create_client('glue')
    
    try:
        response = glue_client.get_databases()
        databases = [database.get('Name') for database in response.get('DatabaseList')]
    except glue_client.exceptions.EntityNotFoundException:
        print('We cannot query databases right now')

    return databases


def get_glue_tables(database_name: str):
    glue_client = create_client('glue')

    try:
        tables = []
        response = glue_client.get_tables(DatabaseName=database_name)
        for table in response.get('TableList', []):
            tables.append(table['Name'])    
    except glue_client.exceptions.EntityNotFoundException:
        print(f"Database '{database_name}' not found.")

    return tables

# Athena functions
def get_all_query_strings():
    athena_client = create_client('athena')
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

