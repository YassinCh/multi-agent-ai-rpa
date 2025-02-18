from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from src.browser.dom.data_structures import SelectorMap

from ..llm_models import default_model


@dataclass
class ElementSelectorDependencies:
    element_map: SelectorMap
    user_field: str


class ElementSelectorResult(BaseModel):
    index: int


element_selector_agent = Agent(
    default_model,
    deps_type=ElementSelectorDependencies,
    result_type=ElementSelectorResult,
    retries=3,
    system_prompt=(
        """
        You are an AI to design to find the correct form field for user data.
        You will be given the user data field you are looking for and a DOM element tree.
        Return only the index as an integer of the correct DOM Tree element 
        input field corresponding to the user data
        if the field doesnt exist respond with -1
        """
    ),
)


@element_selector_agent.system_prompt
async def add_element_tree_and_user_field(ctx: RunContext[ElementSelectorDependencies]):
    return f"""
    The User Data Field You are looking for: \n
    {ctx.deps.user_field} \n
    The Element Selector Map/Tree you are looking for the index of the input field in:
    {ctx.deps.element_map}
    """
