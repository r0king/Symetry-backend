from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.sql.operators import is_
from .roles import Roles

class UserBase(BaseModel):
    username: str
    name:str
    email:str
    contact:str
    role: Roles


class CreateUser(UserBase):
  
    password:str
    
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    contact:Optional[str]
    role: Optional[Roles]
    password: Optional[str]




class User(UserBase):
    id: int
    hashed_password:str
    is_active: bool
    #app_id:int
    #TODO: app


    class Config:
        """Enable ORM mode"""
        orm_mode = True

