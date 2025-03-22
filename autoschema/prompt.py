
def create_prompt(files: dict):
    if not all(key in files for key in ['csv', 'json', 'sql']):
        print("Error: Missing required keys ('csv', 'json', 'sql') in files dictionary.")
        return None

    json_string = f"""
    Table Schemas:
    {files['json']}
    """

    queries_string = '\n'.join(files['sql'])
    sql_string = f"""
    SQL Queries:
    {queries_string}
    """

    csv_data_string = '\n'.join(files['csv'])
    csv_string = f"""
    Data Sample Summaries:
    {csv_data_string}
    """

    initial_prompt = '''
    CONTEXT: You are a database expert.

    OBJECTIVE: Given the following information, your objective is to identify the relations between the tables. You **MUST** follow the next steps

    INSTRUCTIONS:
    1. Analyze table schemas, SQL queries, and data sample summaries (provided below).
    2. Identify relationships between tables based on foreign keys, JOIN clauses, and data patterns.
    3. Output ONLY a JSON dictionary representing the relationships.  No explanations are needed.
    4. Use lowercase for all table and column names in the output.

    OUTPUT FORMAT:
    {
        "customer-orders": [
            {
                "column_src": "column",
                "type_src": "INTEGER",
                "column_dst": "column",
                "type_dst": "INTEGER"
            },
            {
                "column_src": "other_column",
                "type_src": "STRING",
                "column_dst": "other_column",
                "type_dst": "STRING"
            },
            {
                "column_src": "other_other_column",
                "type_src": "DATE",
                "column_dst": "other_other_column",
                "type_dst": "DATE"
            }
        ]
    }

    EXAMPLE:
    INPUT TABLES: {"Customer": [["id", "int"], ["name", "str"], ["product_id", "int"]], "Product": [["id", "int"], ["name", "str"], ["price", "float"]]}
    EXPECTED OUTPUT:
    1 column:
    {
        "customer-product": [
            {
                "column_src": "product_id",
                "type_src": "int",
                "column_dst": "id",
                "type_dst": "int"
            }
        ]
    }
    2 or more columns:
    {
        "customer-product": [
            {
                "column_src": "product_id",
                "type_src": "int",
                "column_dst": "id",
                "type_dst": "int"
            },
            {
                "column_src": "name",
                "type_src": "str",
                "column_dst": "name",
                "type_dst": "str"
            }
        ]
    }
    '''

    prompt = f'''
    {initial_prompt}

    This is the json file:
    {json_string}

    This are the sql queries
    {sql_string}

    This are the csv files
    {csv_string}
    '''

    return prompt
