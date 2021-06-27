#schemas
from typing import List, Optional

from pydantic import BaseModel
class TokenSchema(BaseModel):
    #  session schema
    app_id: int
    user_id: int
    token_id: str

    class Config:
        # Enable ORM mode
        orm_mode = True

class Timestamp_schema(TokenSchema):
    timestamp:str
    


