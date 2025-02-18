"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Dict

from langchain_core.runnables import RunnableConfig

from src.states import AgentState

from ..agents.element_selector import (
    ElementSelectorDependencies,
    element_selector_agent,
)


async def get_element_index_field(
    state: AgentState,
    config: RunnableConfig,
) -> Dict[str, int]:
    """
    Node for testing purposes
    """

    deps = ElementSelectorDependencies(
        element_map=state.browser_state.selector_map, user_field=state.user_field
    )

    response = await element_selector_agent.run(
        "what is the index, just respond with an integer", deps=deps
    )
    index = int(response.data.index)

    return {"element_index": index}
