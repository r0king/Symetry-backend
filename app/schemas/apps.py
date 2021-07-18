"""
Apps schemas
"""
from typing import Optional
import uuid
from pydantic import BaseModel


class CreateApp(BaseModel):
    """Create App Schema"""
    name: str
    secret: str


class UpdateApp(BaseModel):
    """Update App Schema"""
    app_name: Optional[str]
    secret: Optional[str]


class App(BaseModel):
    """Read App Schema"""
    id: uuid.UUID
    name: str
    user_id: int

    class Config:
        """Enable ORM mode"""
        orm_mode = True
