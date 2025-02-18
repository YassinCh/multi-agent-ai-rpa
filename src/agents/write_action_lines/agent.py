from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from src.states import UserData

from ..llm_models import default_model


@dataclass
class WriteActionLineDeps:
    index: int
    user_data: UserData
    user_field: str


class WriteActionLineResult(BaseModel):
    line: str


write_action_line_agent = Agent(
    default_model,
    deps_type=WriteActionLineDeps,
    result_type=WriteActionLineResult,
    retries=3,
    system_prompt=(
        """
        You are an AI to design to write a line of code to set the value of a form field.
        You will be given the user data field you are looking for and a DOM element tree.
        Return only the line of code to set the value of the form field corresponding to the user data
        We use playwright: you can set a field with index x using:
        msg(this is a result message of how it went) = await(cause this is an async thing) 
        BrowserInteract.input_text(5, "User field data", context)
        ONLY respond with the one line: you can assume context exists and BrowserInteract is already imported
        """
    ),
)


@write_action_line_agent.system_prompt
async def add_index_user_field_user_data(ctx: RunContext[WriteActionLineDeps]):
    return f"""
    User Data: {ctx.deps.user_data}
    User Field: {ctx.deps.user_field}
    Index: {ctx.deps.index}
    """
