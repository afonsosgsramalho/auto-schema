import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
import json
import time
from dotenv import load_dotenv, find_dotenv
load_dotenv()

REGION_NAME = os.getenv('AWS_REGION')
ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCES_KEY = os.getenv('AWS_SECRET_ACCES_KEY')


# Clients
def create_client(service: str):
    client = boto3.client(
        service_name=service,
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCES_KEY
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


def get_glue_tables(database_name: str):
    glue_client = create_client('glue')
    try:
        tables = []
        response = glue_client.get_tables(DatabaseName=database_name)

        for table in response.get('TableList', []):
            tables.append(table['Name'])
        
        return tables
    except glue_client.exceptions.EntityNotFoundException:
        print(f"Database '{database_name}' not found.")


# Athena functions
def get_all_query_strings():
    athena_client = create_client('athena')
    query_strings = []
    next_token = None
    num = 1

    while True:

        if next_token:
            response = athena_client.list_query_executions(NextToken=next_token)
        else:
            response = athena_client.list_query_executions()

        query_execution_ids = response.get('QueryExecutionIds')

        for query_execution_id in query_execution_ids:
            query_details = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            query_string = query_details['QueryExecution']['Query'].strip('\n').strip()
            query_strings.append(query_string)

        print('current_token', num,  next_token)
        num += 1

        next_token = response.get('NextToken', None)

        if not next_token:
            break

    return query_strings


teste = get_all_query_strings()
print(teste)