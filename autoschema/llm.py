from typing import Dict
from mistralai import Mistral
import os

from config import Config
from prompt import create_prompt
from exceptions import ModelTypeError

MAX_TOKEN = 128000

class LLM(Config):
    def __init__(self, is_locally:bool):
        super().__init__()
        self.is_locally = is_locally

        if not hasattr(self, 'client'):
            self.client = Mistral(api_key=self.api_key)


    def check_size(self, files:Dict[str, str]):
        if not self.is_locally:
            pass
        else:
            raise ModelTypeError('This model only runs thorugh API Service')
        

    def chat_completion(self, files:Dict[str, str]):
        if not self.is_locally:
            chat_response = self.client.chat.complete(
                model = self.model,
                messages = [
                    {
                        'role': 'user',
                        'content': create_prompt(files)
                    },
                ], 
                stream=False,
                response_format = {
                    'type': 'json_object'
                }
            )

            return chat_response.choices[0].message.content
        else:
            raise ModelTypeError('This model only runs thorugh API Service')


    def _install_model_locally(self):
        if self.is_locally:
            #Integreate with http requests to local model
            pass