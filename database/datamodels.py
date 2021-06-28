#schemas
from typing import List, Optional

from pydantic import BaseModel
class TokenCreate(BaseModel):
    #  session schema
    app_id: int
    user_id: int
class TokenSchema(TokenCreate)
    timestamp:str
    token_id: str
    class Config:
        # Enable ORM mode
        orm_mode = True

    


