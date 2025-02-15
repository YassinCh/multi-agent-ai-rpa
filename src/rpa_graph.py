"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Dict, List, Literal, cast
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from src.configuration import Configuration
from src.states import InputState, AgentState
from langgraph.graph import StateGraph, START, END
import sys
from src.nodes import analyze_form_node


def route_next_step(state: AgentState) -> Literal["__end__"]:
    """
    This is the router, which will based on the state decide on what the next node is
    This might already be included in the state, or might be
    done different for now it return to end
    """
    return END


builder = StateGraph(AgentState, input=InputState, config_schema=Configuration)

# Add all the nodes
builder.add_node("analyze_form", analyze_form_node)

# Set the entrypoint
builder.add_edge("__start__", "analyze_form")

# Add conditional edges
builder.add_conditional_edges("analyze_form", route_next_step)

graph = builder.compile()
graph.name = "AI RPA Agent"
