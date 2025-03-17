PROMPTS = {
    'Context':
    '''
    The objective of this prompt is to understand the relationship between tables i will provide you.
    For that i will provide the structure of the tables as well as the format i want the output to be in.
    I dont want any explanation of the thought process, i want the response like i will tell you.
    ''',
    'StructureResponse':
    '''
    This is an example of structure i will provide you:
    Input
    {"Customer": [["id", "int"], ["name", "str"], ["product_id", "int"]], "Product": [["id", "int"], ["name", "str"], ["price", "float"]]}
    I want that the output to be like this:
    Output
    {"Customer-Product": [['product_id', 'id']]}
    Note: This output can have multiple relationships between tables, and each relatinship can have more than one field connecting both tables.
    Return everything in lowercase letters
    ''',
    'TablesData':
    '''
    '''
}

def create_prompt(files):
    if files.type == 'json':
        json = f'''
        Here are the json files:
        {files.content}
        '''
    elif files.type == 'sql':
        sql = f'''
        Here are the sql queries:
        {files.content}        
        '''
    else:
        csv = f'''
        Here are the csv files:
        {files.content}
        '''
    prompt = f'''
    {json}
    {sql}
    {csv}
    '''