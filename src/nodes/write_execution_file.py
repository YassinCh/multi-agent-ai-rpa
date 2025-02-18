"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Dict

from langchain_core.runnables import RunnableConfig

from src.browser import BrowserState
from src.states import AgentState
from src.tools import create_execution_file


async def write_execution_file(
    state: AgentState,
    config: RunnableConfig,
) -> Dict[str, BrowserState]:
    """
    Write the action history to an execution file
    """
    await create_execution_file(state.action_history, state.url)
    next_step = "__end__"

    return {
        "next_step": next_step,
        "proccessed_fields": state.proccessed_fields,
        "browser_context": state.browser_context,
    }
