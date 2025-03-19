
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
    {"table1-table2": [["column_table1", "column_table2"], ...], ...}

    EXAMPLE:
    INPUT TABLES: {"Customer": [["id", "int"], ["name", "str"], ["product_id", "int"]], "Product": [["id", "int"], ["name", "str"], ["price", "float"]]}
    EXPECTED OUTPUT: 
    1 column          -> {"customer-product": [["product_id", "id"]]}
    2 or more columns -> {"customer-product": [["product_id", "id"], ["name", "name"]]}
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

    print(prompt)
    return prompt
