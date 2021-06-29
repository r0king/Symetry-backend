"""
Logs Schemas
"""
from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class CreateLog(BaseModel):
    """Create Log Schema"""
    app_id: Optional[uuid.UUID]
    user_id: Optional[int]
    message: str


class Log(CreateLog):
    """Read Log Schema"""
    timestamp: datetime
    id: int

    class Config:
        """Enable ORM mode"""
        orm_mode = True
