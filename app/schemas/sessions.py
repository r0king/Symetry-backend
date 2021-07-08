"""
Session schemas
"""
from datetime import datetime
from pydantic import BaseModel


class SessionCreate(BaseModel):
    """Session create schema"""

    user_id: int
    token: str
    save_session: bool = True


class SessionSchema(SessionCreate):
    """Session Complete Schema"""

    id: int
    timestamp: datetime

    class Config:
        """Enable ORM mode"""
        orm_mode = True
