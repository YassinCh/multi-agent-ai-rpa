from pydantic import BaseModel
from typing import Dict, Any


class UserData(BaseModel):
    """Model for normalized user data"""

    fields: Dict[str, Any]


class FormField(BaseModel):
    """Model for form field information"""

    name: str
    type: str
    id: str | None = None
    label: str | None = None
    placeholder: str | None = None
