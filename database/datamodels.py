"""
All the schemas for Symmetry
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.sql.expression import true


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


class SessionRead(BaseModel):
    # Session read schema
    id: Optional[int] = None
    user_id: int


class SessionCreate(SessionRead):
    #  session schema for create

    id: int
    save_session: bool = true
    # timestamp: datetime
    
    class Config:
        # Enable ORM mode
        orm_mode = True

class SessionSchema(SessionRead):
    #  session schema

    id: int
    save_session: bool = true
    timestamp: datetime
    hashed_token:str
    class Config:
        # Enable ORM mode
        orm_mode = True
