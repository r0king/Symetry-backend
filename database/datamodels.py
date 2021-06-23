"""
All the schemas for Symmetry
"""
from datetime import datetime
from pydantic import BaseModel


class CreateLog(BaseModel):
    """Create Log Schema"""
    app_id: int
    user_id: int
    message: str


class Log(CreateLog):
    """Read Log Schema"""
    time: datetime
    id: int

    class Config:
        """Enable ORM mode"""
        orm_mode = True


class SessionSchema(BaseModel):
    #  session schema
    app_id: int
    user_id: int

    class Config:
        # Enable ORM mode
        orm_mode = True


class SessionCreate(SessionSchema):
    #  session create schema
    token_id: str
