from diagram import Diagram, Class, Relationship
from parser import create_json_file, create_sql_file, create_csv_file
from model import chat_completion
from sources.aws import AWSClientManager
from files import create_files_folder


# def create_relationships():
#     content = read_json('schema/example.json')
#     response = call_api(content)
#     response_parsed = read_output(response)

#     diagram = Diagram()

#     # Create classes
#     for table in content:
#         diagram.add_class(Class(table, content[table]))
    
#     # Create relationships
#     for table in response_parsed:
#         table1, table2 = table.split('-')
#         diagram.add_relationship(Relationship(table1, table2, '||--o{', response_parsed[table][0][0]))
        
#     return diagram


def store_files(file_path:str):
    #create folder where files are going to be stored
    create_files_folder(file_path)

    #1st step - get fields of tables in json
    aws = AWSClientManager()
    tables = aws.get_glue_tables('silver')
    tables_fields = {}
    for table in tables:
        tables_fields[table] = aws.get_table('silver', table)

    create_json_file(file_path, 'tables.json', tables_fields)

    #2nd step - get queries in sql file
    query_strings = aws.get_all_query_strings()
    create_sql_file(file_path, 'queries.sql', query_strings)

    #3rd step - get csv files with samples of data
    query_data = aws.get_query_data('silver', 'deputies', 's3://evs-query-output/Unsaved/', 10)
    create_csv_file(file_path, 'file.csv', query_data)


def main():
    pass

if __name__ == '__main__':
    print(main())