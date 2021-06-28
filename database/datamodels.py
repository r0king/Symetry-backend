"""
Datamodels aka Schema
"""
from typing import Optional
from pydantic import BaseModel
from .roles import Roles


class UserBase(BaseModel):
    """
    Base User Schema
    """
    username: str
    name:str
    email:str
    contact:str
    role: Roles


class CreateUser(UserBase):
    """
    Create User Schema
    """
    password:str



class UserUpdate(BaseModel):
    """
    Update user schema
    """
    username: Optional[str]
    email: Optional[str]
    contact:Optional[str]
    role: Optional[Roles]
    password: Optional[str]



class User(UserBase):
    """
    Full User Schema(As in DB)
    """
    id: int
    hashed_password:str
    is_active: bool

    class Config:
        """Enable ORM mode"""
        orm_mode = True
