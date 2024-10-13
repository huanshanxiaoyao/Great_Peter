
from openai import OpenAI

class BaseModel():
    def __init__(self, api_key, base_url, model_name):
        self.api_key= api_key
        self.base_url = base_url
        #self.client = OpenAI(api_key=api_key, base_url=self.base_url)
        self.client = OpenAI(api_key="sk-c883019d2db04d458026a16318a3491f", base_url="https://api.deepseek.com")

        self.model = model_name

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
