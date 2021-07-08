"""
Token schemas
"""
from datetime import datetime
import uuid
from pydantic import BaseModel


class VerifyToken(BaseModel):
    """
    Token Verify schema
    """
    app_id: uuid.UUID
    token: str


class TokenCreate(BaseModel):
    """
    Token Create schemas
    """
    app_id: uuid.UUID
    user_id: int

    # Store the same timestamp used while hashing the token
    timestamp: datetime


class TokenSchema(TokenCreate):
    """
    Token Full Schema
    """
    id: uuid.UUID

    class Config:
        """Enable ORM Mode"""
        orm_mode = True
