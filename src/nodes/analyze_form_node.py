"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Dict, List, Literal, cast
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from src.configuration import Configuration
from src.states import InputState, AgentState, FormField
from langgraph.graph import StateGraph, START, END
from src.tools import analyze_form


async def analyze_form_node(
    state: AgentState,
    config: RunnableConfig,
) -> Dict[str, List[FormField]]:
    """
    Node for analyzing form structure. This is the setup for the manager
    The manager which will not have an LLM Agent but will manage the flow!
    It will manage the current rules in the state when it gets a (already validated)
    rule back, moves to the next user data_field, and
    adapt the current analyzed field in the state to then
    hand it over to the correct agent
    """
    try:
        configuration = Configuration.from_runnable_config(config)
        form_fields = await analyze_form(url=state.url, config=configuration)
        return {"form_fields": form_fields}
    except Exception as e:
        state.error = str(e)
        return {"form_fields": []}
