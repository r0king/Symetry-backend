"""
Datamodels aka Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .roles import Roles


# User Schemas

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


# App Schemas

class CreateApp(BaseModel):
    """Create App Schema"""
    user_id: str
    name: str
    app_name:str

class App(CreateApp):
    """Read App Schema"""
    app_id: str
    app_secret: str

    class Config:
        """Enable ORM mode"""
        orm_mode = True


class UpdateApp(BaseModel):
    """Update App Schema"""
    app_name: Optional[str]


# Log Schemas

class CreateLog(BaseModel):
    """Create Log Schema"""
    app_id: int
    user_id: int
    message: str


class Log(CreateLog):
    """Read Log Schema"""
    timestamp: datetime
    id: int

    class Config:
        """Enable ORM mode"""
        orm_mode = True
