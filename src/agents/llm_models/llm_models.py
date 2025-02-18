from pydantic_ai.models.openai import OpenAIModel
from env import env

reasoner_model = OpenAIModel("o3-mini", api_key=env.OPENAI_API_KEY)
default_model = OpenAIModel("gpt-4o-mini", api_key=env.OPENAI_API_KEY)
