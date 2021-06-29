"""
Apps schemas
"""
from typing import Optional
import uuid
from pydantic import BaseModel


class CreateApp(BaseModel):
    """Create App Schema"""
    user_id: int
    name: str
    secret: str


class UpdateApp(BaseModel):
    """Update App Schema"""
    app_name: Optional[str]
    secret: Optional[str]


class App(CreateApp):
    """Read App Schema"""
    id: uuid.UUID

    class Config:
        """Enable ORM mode"""
        orm_mode = True
