from models.llama import LLama3
from models.open_ai import GPT4
from models.deep_seek import DeepSeek2
from models.constants import DEEPSEEK_KEY, DEEPSEEK_URL


class ModelFactory:
    @staticmethod
    def get_model_class(model_name):
        if model_name == "DeepSeek":
            return DeepSeek2(DEEPSEEK_KEY, DEEPSEEK_URL)
        elif model_name == "Llama3":
            return LLama3
        elif model_name == "GPT4":
            return GPT4
        else:
            raise Exception(f"Unknown model name {model_name}")
