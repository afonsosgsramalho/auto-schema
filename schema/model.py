from mistralai import Mistral
import os
from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv('MISTRAL_MODEL')
API_KEY = os.getenv("MISTRAL_API_KEY")

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


def chat_completion(content: str):
    with Mistral(
        api_key=API_KEY,
    ) as mistral:

        chat_response = mistral.chat.complete(model=MODEL, messages=[
            {
                "content": f'{PROMPTS['Context']} {PROMPTS['StructureResponse']}. Content: {content}',
                "role": "user",
            },
        ], stream=False)

    return chat_response.choices[0].message.content


def upload_file(file):
    file_name = os.path.basename(file)
    with Mistral(
        api_key=API_KEY,
    ) as mistral:

        response = mistral.files.upload(file={
            "file_name": file,
            "content": open(file, "rb"),
        })

        print(response)
    
    return response
