from typing import Optional, List, Dict

from diagram import Diagram, Class, Relationship
from file import FileManager, FileReader, FileExtractor
from llm import LLM
from sources.aws import AWSClientManager
from render import mm


def store_files(
    file_extractor:FileExtractor,
    file_manager:FileManager,
    database:str,
    path:Optional[str]
):
    # 1. Extract Table Schemas (JSON)
    tables_fields = file_extractor.extract_table_schemas(database)
    file_manager.create_json_file(path, "tables.json", tables_fields)

    # 2. Extract SQL Queries (Text)
    query_strings = file_extractor.extract_sql_queries()
    file_manager.create_text_file(path, "queries_sql.txt", query_strings)

    # 3. Extract Data Samples (CSV)
    tables_data = file_extractor.extract_data_samples(database, path)

    output = {
        "json": tables_fields,
        "sql": query_strings,
        "csv": tables_data,
    }

    return output


def call_llm(
    llm:LLM, 
    files:Dict[str, str]
):
    if len(files) < 3: 
        raise ValueError('Not enough type of files')
    
    response = llm.chat_completion(files)

    return response


def generate_diagram(
    file_reader:FileReader, 
    table_list: Dict[str, List[List[str]]],
    chat_response: Dict[str, List[List[str]]]
):

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
    aws_client = AWSClientManager()
    file_manager = FileManager(file_path)
    file_reader = FileReader()
    file_extractor = FileExtractor(
        aws_client=aws_client,
        file_manager=file_manager,
        bucket_output='s3://evs-query-output/Unsaved/'
    )

    llm = LLM(
        is_locally=False
    )

    files = store_files(
        file_extractor=file_extractor, 
        file_manager=file_manager, 
        database='silver', 
        path='autoSchema')
    llm_response = call_llm(llm, files)

    diagram = str(generate_diagram(file_reader, files.get('json'), llm_response))

    print()
    print(generate_diagram(file_reader, files.get('json'), llm_response))
    mm(diagram)

