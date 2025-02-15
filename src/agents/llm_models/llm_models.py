from pydantic_ai.models.openai import OpenAIModel
from core import env


reasoner_model = OpenAIModel("o3-mini", api_key=env.openai_api_key)
default_model = OpenAIModel("gpt-4o-mini", api_key=env.openai_api_key)

