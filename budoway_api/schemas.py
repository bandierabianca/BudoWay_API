from pydantic import BaseModel
from sqlmodel import SQLModel

class UserRegister(SQLModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str
