from pydantic import BaseModel
from typing import Dict, Any, List, Literal

import json
from .data import UserData, FormField


class AgentState(BaseModel):
    """Model for agent state"""

    url: str
    user_data: UserData
    form_fields: List[FormField] = []
    field_mappings: Dict[str, Dict[str, Any]] = {}
    success: bool = False
    error: str | None = None
    current_step: str = "analyze_form"


class InputState(BaseModel):
    """Model for input state"""

    url: str
    user_data: Dict[str, Any]


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
