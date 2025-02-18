"""Define the form filling agent graph."""

from __future__ import annotations

from textwrap import indent
from typing import Dict, List, Literal, cast

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from src.browser import Browser, BrowserConfig, BrowserContext, BrowserState
from src.configuration import Configuration
from src.states import AgentState, InputState
from src.tools import create_execution_file, get_page_information, run_line


async def main_flow_manager(
    state: AgentState,
    config: RunnableConfig,
) -> Dict[str, BrowserState]:
    """
    The goal of the flow manager is determining the next user_field
    Whether it should be processed or not
    And process the result of the other agents
    Also this will add the current page DOM Tree to the context
    This will also setup the browser context and add that to the state
    """
    # TODO: Add browser config in Runnable Config :)
    # configuration = Configuration.from_runnable_config(config)
    browser_config = BrowserConfig(headless=True, disable_security=False)

    ##### Get the browser setup #############
    # TODO: this gets a new setup everything main flow is called
    # TODO: BAD I need a way to not make this happen
    # TODO: e.g. make everything a singleton including context

    if state.browser_context is None:
        browser = Browser(config=browser_config)

        context = await browser.new_context()
        state.browser_context = context

    # TODO: When do I get the state of the browser?? Cause multiple pages I cant get it just once
    browser_state = await get_page_information(
        url=state.url, context=state.browser_context
    )
    action_history = state.action_history
    action_line = state.action_line

    if state.element_index == -1:
        # This means the field doesnt exist
        state.proccessed_fields.append(state.user_field)
        user_field = None
    else:
        if action_line:
            try:
                await run_line(state.url, action_line)
                state.proccessed_fields.append(state.user_field)
                action_history.append(action_line)
                action_line = None
                user_field = None

            except Exception as e:
                # TODO: Route this to the debug agent together with error
                next_step = "__end__"

    #### Get the next field #####
    for field in state.user_data.fields.keys():
        if field not in state.proccessed_fields:
            user_field = field
            next_step = "get_element_index_field"
            break
    if user_field is None:
        # All fields have been proccessed
        # TODO: All fields on this page have been proccessed
        # this should link to finding and proccessing the next page
        await create_execution_file(action_history, state.url)
        next_step = "__end__"

    return {
        "browser_state": browser_state,
        "user_field": user_field,
        "next_step": next_step,
        "proccessed_fields": state.proccessed_fields,
        "action_history": action_history,
        "action_line": action_line,
        "browser_context": state.browser_context,
    }
