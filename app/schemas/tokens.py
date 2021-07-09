"""
Token schemas
"""
from datetime import datetime
import uuid
from pydantic import BaseModel



class TokenRequestSchema(BaseModel):
    """
    Schema for user requesting token with token_id
    """
    token_id: uuid.UUID


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


class TokenSchema(TokenCreate):
    """
    Token Full Schema
    """
    id: uuid.UUID
    timestamp: datetime

    class Config:
        """Enable ORM Mode"""
        orm_mode = True
