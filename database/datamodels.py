"""
All the schemas for Symmetry
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

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

class SessionSchema(SessionRead):
    #  session schema
    token:str
    save_session:bool
    timestamp:str

    class Config:
        # Enable ORM mode
        orm_mode = True
