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

    csv_string = f"""
    Data Sample Summaries:
    {files['csv']}
    """

    prompt = f"""
    You are a database expert. Given the following information, your objective is to identify the relations between the tables. You **MUST** follow these steps:

    1.  **Analyze Schemas:** Carefully review the table schemas provided below. Identify potential primary key and foreign key relationships based on column names and data types.
    2.  **Analyze SQL Queries:** Examine the SQL queries for JOIN clauses, WHERE clauses (especially those comparing columns), and GROUP BY clauses.  These indicate how tables are related.
    3.  **Analyze Data Sample Summaries:** Look for patterns in the data sample summaries that confirm or refute potential relationships.
    4.  **Reasoning:** For each potential relationship, explain **step by step** why you believe it exists.  Consider the schemas, SQL queries, and data summaries.  Be specific about the columns involved and the type of relationship (one-to-many, many-to-many, etc.).  Describe any limitations or uncertainties in your reasoning.  Format each reasoning as:
        ```
        Table1: [Table Name]
        Table2: [Table Name]
        Column1: [Column Name]
        Column2: [Column Name]
        Relationship Type: [Type]
        Confidence: [Confidence Level - High, Medium, Low]
        Reasoning: [Step-by-step explanation]
        ```
    5.  **JSON Output:** Based on your reasoning, output the relationships in JSON format.  Include the reasoning for each relationship:

    ```json
    [
        {{
            "table1": "table_name1",
            "table2": "table_name2",
            "column1": "column_name1",
            "column2": "column_name2",
            "relationship_type": "one-to-many",
            "confidence": 0.8,
            "reasoning": "Explanation of why the LLM believes this relationship exists"
        }}
    ]
    ```

    {json_string}

    {sql_string}

    {csv_string}

    Important:  After carefully following the steps above and providing detailed reasoning for each potential relationship, provide the final JSON output **ONLY** within the ```json ... ``` tags. Do not include any surrounding text.
    """

    return prompt
