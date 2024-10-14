import os
from openai import OpenAI
from models.base_model import BaseModel

class GPT4(BaseModel):
    def __init__(self, api_key):
        self.model_name = "gpt-4o-mini"
        super().__init__(api_key, "", self.model_name) #TODO
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    def request(self, question):
        req_content = question
        role_setting = " You are a helpful assistant"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": role_setting},
                {"role": "user", "content": req_content},
            ],
            stream=False
        )
        message_content = response.choices[0].message.content
        return message_content


if __name__ == "__main__":
    model_name = "gpt-4o-mini"
    print(os.getenv("OPENAI_KEY"))
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello, give a short introduction about Peter Great"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
