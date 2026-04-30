from typing import Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int
    price: float

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class config:
        # orm_mode = True / we use this attribute for Pydantic version less than 2.X
        from_attribute = True
# - - - - - - - - - - - - - - 
class UserBase(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

class UserCreate(UserBase):
    name: str
    email: str
    role: str
    password: str

class UserResponse(UserBase):
    id: int
    name:str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attribute = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None