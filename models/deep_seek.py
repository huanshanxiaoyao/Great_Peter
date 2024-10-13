# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from models.base_model import BaseModel

class DeepSeek2(BaseModel):
    def __init__(self, api_key, base_url):
        super().__init__(api_key, base_url, "deepseek-chat")





if __name__ == "__main__":
    client = OpenAI(api_key="sk-c883019d2db04d458026a16318a3491f", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
