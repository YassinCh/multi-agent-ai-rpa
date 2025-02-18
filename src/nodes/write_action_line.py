"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Dict, List
from langchain_core.runnables import RunnableConfig

from src.states import AgentState


async def write_action_line(
    state: AgentState,
    config: RunnableConfig,
) -> Dict[str, str]:
    """
    Node to add Action Line, this will become more complicated in the future
    """
    value = state.user_data.fields[state.user_field]
    line = (
        f"await BrowserInteract.input_text({state.element_index}, '{value}', context)"
    )

    return {"action_line": line}
