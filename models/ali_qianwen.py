
from openai import OpenAI
from models.base_model import BaseModel

class QianWen(BaseModel):
    def __init__(self, api_key, base_url):
        self.model_name = "qwen-plus" # # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        super().__init__(api_key, base_url, self.model_name)





if __name__ == "__main__":
    client = OpenAI(api_key="sk-9e8b542423f4478a907699e762eb6bba", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello, tell me more about you"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
