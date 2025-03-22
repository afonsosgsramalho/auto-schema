from typing import Dict, List, Literal, Optional, Union
import os

from mistralai import Mistral
from mistralai.models import File

from config import Config
from prompt import create_prompt

MAX_TOKEN = 128000

class LLM(Config):
    def __init__(self):
        super().__init__()

        if not hasattr(self, 'client'):
            self.client = Mistral(api_key=self.api_key)

    def check_size(self, files: dict):
        pass

    def chat_completion(self, files:dict):
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


