import json

from diagram import Diagram, Class, Relationship
from creator import FileManager, FileReader
from llm import LLM
from sources.aws import AWSClientManager


def store_files(file:FileManager, database:str, bucket_output:str, path=None):
    # 1st step - get fields of tables in json
    aws = AWSClientManager()
    tables = aws.get_glue_tables(database)
    tables_fields = {}
    for table in tables:
        tables_fields[table] = aws.get_table('silver', table)
    file.create_json_file(path, 'tables.json', tables_fields)

    # 2nd step - get queries in sql file
    query_strings = aws.get_all_query_strings()
    file.create_text_file(path, 'queries_sql.txt', query_strings)

    # 3rd step - get csv files with samples of data
    tables_data = []
    file_reader = FileReader()
    # query_data = aws.get_query_data('silver', 'deputies', 's3://evs-query-output/Unsaved/', 10)
    for table in tables:
        query_data = aws.get_query_data(database, table, bucket_output)
        table_data = file_reader.dataframe_to_prompt(query_data)
        tables_data.append(table_data)
        file.create_csv_file(path, 'file.csv', query_data)

    output = {
        'json': tables_fields,
        'sql': query_strings,
        'csv': tables_data
    }
    
    return output


def call_llm(llm:LLM, files:dict):
    if len(files) < 3: 
        raise ValueError('Not enough type of files')
    
    response = llm.chat_completion(files)

    return response


def generate_diagram(file_reader: FileReader, chat_response: dict[str, list[list[str]]]) -> Diagram:
    content = file_reader.read_output(chat_response)
    diagram = Diagram()

    for connection in content:
        col_connections = content[connection]
        table_src, table_dst = connection.split('-')

        class_src_att = [[col_connection['column_src'], 
                          col_connection['type_src']] 
                          for col_connection in col_connections]
        
        class_dst_att = [[col_connection['column_dst'], 
                          col_connection['type_dst']] 
                          for col_connection in col_connections]
        
        for col_connection in col_connections:
            diagram.add_relationship(Relationship(table_src, table_dst, '||--o{', col_connection['column_src']))
        
        if not diagram.get_class(table_src):
            diagram.add_class(Class(table_src, class_src_att))

        if not diagram.get_class(table_dst):
            diagram.add_class(Class(table_dst, class_dst_att))

    return diagram


def mermaid():
    file_path = 'data'
    file = FileManager(file_path)
    file_reader = FileReader()
    llm = LLM()

    files = store_files(file, 'silver', 's3://evs-query-output/Unsaved/', 'teste')
    response = call_llm(llm, files)
    # print(response)
    print()
    print(generate_diagram(file_reader, response))

