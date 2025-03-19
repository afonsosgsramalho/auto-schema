from dotenv import load_dotenv, find_dotenv
import os

ENV_VARS = [
    'MISTRAL_MODEL',
    'MISTRAL_API_KEY'
]

class Config:
    def __init__(self):
        if not self.are_env_vars_set():
            load_dotenv(find_dotenv())

        self.model = os.getenv('MISTRAL_MODEL')
        self.api_key = os.getenv('MISTRAL_API_KEY')

    def are_env_vars_set(self):
        return all(var in os.environ for var in ENV_VARS)
    
    def display_config(self):
        print(f'Mistral Model: {self.model}')
        print(f':Mistral api key {self.api_key}')
