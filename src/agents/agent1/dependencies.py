from pydantic_ai.agents import AsyncOpenAI

@dataclass
class PydanticAIDeps:
    openai_client: AsyncOpenAI
    reasoner_output: str
