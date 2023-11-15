from pydantic import BaseModel, EmailStr
from sqlalchemy.dialects.postgresql import UUID


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    

class RequestCreate(BaseModel):
    user_id : int
    food: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str