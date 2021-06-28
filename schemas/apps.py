"""
Apps schemas
"""
from typing import Optional
from pydantic import BaseModel


class CreateApp(BaseModel):
    """Create App Schema"""
    user_id: str
    name: str
    app_name:str


class UpdateApp(BaseModel):
    """Update App Schema"""
    app_name: Optional[str]


class App(CreateApp):
    """Read App Schema"""
    app_id: str
    app_secret: str

    class Config:
        """Enable ORM mode"""
        orm_mode = True
