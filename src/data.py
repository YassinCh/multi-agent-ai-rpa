from pydantic import BaseModel
from typing import Dict, Any


class UserData(BaseModel):
    """Model for normalized user data"""

    fields: Dict[str, Any]
