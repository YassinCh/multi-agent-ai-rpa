"""Define the form filling agent graph."""

from __future__ import annotations

from typing import Literal

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from src.configuration import Configuration
from src.nodes import (
    get_element_index_field,
    main_flow_manager,
    write_action_line,
    write_execution_file,
)
from src.states import AgentState, InputState


def route_next_step(
    state: AgentState,
) -> Literal["get_element_index_field", "write_execution_file", "__end__"]:
    """
    This is the router, which will based on the state decide on what the next node is
    This might already be included in the state, or might be
    done different for now it return to end
    """
    return state.next_step


builder = StateGraph(AgentState, input=InputState, config_schema=Configuration)

# Nodes
builder.add_node("main_flow_manager", main_flow_manager)
builder.add_node("get_element_index_field", get_element_index_field)
builder.add_node("write_action_line", write_action_line)
builder.add_node("write_execution_file", write_execution_file)

# Edges
builder.add_edge("__start__", "main_flow_manager")
builder.add_conditional_edges("main_flow_manager", route_next_step)
builder.add_edge("get_element_index_field", "write_action_line")
builder.add_edge("write_action_line", "main_flow_manager")
builder.add_edge("write_execution_file", "__end__")


graph = builder.compile()
graph.name = "AI RPA Agent"
