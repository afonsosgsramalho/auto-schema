import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

model = os.getenv('MISTRAL_MODEL')
api_key = os.getenv("MISTRAL_API_KEY")


def call_api(content: str):
    with Mistral(
        api_key=api_key,
    ) as mistral:

        res = mistral.chat.complete(model=model, messages=[
            {
                "content": content,
                "role": "user",
            },
        ], stream=False)

        #  Handle response
    return res


response = call_api("Who is the best Sporting CP player ever? Answer in one short sentence.")
print(response)