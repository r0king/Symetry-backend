#schemas
from typing import List, Optional
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

class CreateApp(BaseModel):
    """Create App Schema"""
    user_id: str
    password:str
    name: str
    email: str
    contact: str
    app_name:str

class App(CreateApp):
    """Read App Schema"""
    app_id: str
    app_secret: str

    class Config:
        """Enable ORM mode"""
        orm_mode = True


class HTTPError(BaseModel):
    detail: str


class updateUser(BaseModel):
    user_id: Optional[str]
    password:Optional[str]
    name: Optional[str]
    email: Optional[str]
    contact: Optional[str]
    

