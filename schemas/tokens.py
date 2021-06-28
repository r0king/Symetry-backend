"""
Token schemas
"""
from datetime import datetime
from pydantic import BaseModel


class TokenCreate(BaseModel):
    """
    Token Create schemas
    """
    app_id: int
    user_id: int

    # Store the same timestamp used while hashing the token
    timestamp: datetime


class TokenSchema(TokenCreate):
    """
    Token Full Schema
    """
    token_id: str

    class Config:
        """Enable ORM Mode"""
        orm_mode = True
