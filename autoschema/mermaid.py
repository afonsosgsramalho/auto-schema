from diagram import Diagram, Class, Relationship
from file import FileManager, FileReader
from llm import LLM
from sources.aws import AWSClientManager
from exceptions import DataExtractionError


def _extract_table_schemas(
        aws_client: AWSClientManager,
        database: str
) -> dict[str, str]:
    try:
        tables = aws_client.get_glue_tables(database)
        tables_fields = {}
        
        for table in tables:
            tables_fields[table] = aws_client.get_table('silver', table)
        
        return tables_fields
    except Exception as e:
        raise DataExtractionError(f"Failed to extract SQL queries: {e}") from e


def _extract_sql_queries(aws_client: AWSClientManager) -> list[str]:
    try:
        return aws_client.get_all_query_strings()
    except Exception as e:
        raise DataExtractionError(f"Failed to extract SQL queries: {e}") from e
    

def _extract_data_samples(
    file_manager: FileManager,
    aws_client: AWSClientManager,
    database: str,
    bucket_output: str,
    path: str,
) -> list[str]:
    tables_data = []
    file_reader = FileReader()

    try:
        tables = aws_client.get_glue_tables(database)

        for table in tables:
            query_data = aws_client.get_query_data(database, table, bucket_output)
            table_data = file_reader.dataframe_to_prompt(query_data)
            tables_data.append(table_data)
            file_manager.create_csv_file(path, f"{table}.csv", query_data)
        return tables_data

    except Exception as e:
        raise DataExtractionError(f"Failed to extract data samples: {e}") from e
    

def store_files(
    file_manager: FileManager,
    database: str,
    bucket_output: str,
    path: str = None,
) -> dict[str, str]:
    aws_client = AWSClientManager()

    # 1. Extract Table Schemas (JSON)
    tables_fields = _extract_table_schemas(aws_client, database)
    file_manager.create_json_file(path, "tables.json", tables_fields)

    # 2. Extract SQL Queries (Text)
    query_strings = _extract_sql_queries(aws_client)
    file_manager.create_text_file(path, "queries_sql.txt", query_strings)

    # 3. Extract Data Samples (CSV)
    tables_data = _extract_data_samples(
        file_manager, aws_client, database, bucket_output, path
    )

    output = {
        "json": tables_fields,
        "sql": query_strings,
        "csv": tables_data,
    }

    return output


def call_llm(llm:LLM, files:dict):
    if len(files) < 3: 
        raise ValueError('Not enough type of files')
    
    response = llm.chat_completion(files)

    return response


def generate_diagram(
    file_reader: FileReader, 
    table_list: dict[str, list[list[str]]],
    chat_response: dict[str, list[list[str]]]) -> Diagram:

    content = file_reader.read_output(chat_response)
    diagram = Diagram()

    for table in table_list:    
        if not diagram.get_class(table):
            diagram.add_class(Class(table, table_list.get(table)))

    for connection in content:
        col_connections = content[connection]
        table_src, table_dst = connection.split('-')
        
        for col_connection in col_connections:
            diagram.add_relationship(Relationship(table_src, table_dst, '||--o{', col_connection['column_src']))
        

    return diagram


def mermaid():
    file_path = 'data'
    file = FileManager(file_path)
    file_reader = FileReader()
    llm = LLM()

    files = store_files(file, 'silver', 's3://evs-query-output/Unsaved/', 'autoSchema')
    llm_response = call_llm(llm, files)

    print()
    print(generate_diagram(file_reader, files.get('json'), llm_response))

