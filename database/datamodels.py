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


class SessionSchema(BaseModel):
    #  session schema
    id: Optional[int] = None
    user_id: int

    class Config:
        # Enable ORM mode
        orm_mode = True

class SessionReturn(SessionSchema):
    # Session return schema
    token:str
    save_session:bool
    timestamp:str
