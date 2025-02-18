from pydantic import BaseModel
from typing import Dict, Any, List, Literal, Optional
from dataclasses import field
import json
from .data import UserData
from .browser.context import BrowserState, BrowserContext


class AgentState(BaseModel):
    """Model for agent state"""

    # TODO: Clean and add where needed

    url: str
    user_data: UserData
    user_field: Optional[str] = ""
    element_index: Optional[int] = None
    action_line: Optional[str] = None
    action_history: List[str] = field(default_factory=list)
    proccessed_fields: List[str] = field(default_factory=list)
    next_step: str = "__end__"
    browser_state: Optional[BrowserState] = None
    browser_context: Optional[BrowserContext] = None

    success: bool = False
    error: str | None = None


class InputState(BaseModel):
    """Model for input state"""

    url: str
    user_data: UserData


def parse_user_data(raw_data: Any) -> UserData:
    """Parse and normalize user data from any format"""
    if isinstance(raw_data, str):
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
    elif isinstance(raw_data, dict):
        data = raw_data
    else:
        raise ValueError("Unsupported data format")

    return UserData(fields=data)
