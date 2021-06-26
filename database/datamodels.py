#schemas
from typing import List, Optional
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

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


class HTTPError(BaseModel):
    detail: str


class updateApp(BaseModel):
    user_id: Optional[str]
    password:Optional[str]
    name: Optional[str]
    email: Optional[str]
    contact: Optional[str]
    app_name: Optional[str]
    
    

