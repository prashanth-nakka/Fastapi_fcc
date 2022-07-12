from typing import Optional
from pydantic import BaseModel, EmailStr
from .database import Base
from datetime import datetime


# Schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime
    # optional fileds
    # # rating: Optional[int] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class CreatePost(PostBase):
    pass
    # title: str
    # content: str
    # published: bool = True
    # optional fileds
    # rating: Optional[int] = None


class UpdatePost(BaseModel):
    pass
    # title: str
    # content: str
    # published: bool = True
    # optional fileds
    # rating: Optional[int] = None


# Reponse Class to the user
class user_response(PostBase):
    id: int
    created_at: datetime

    class Config:
        '''Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
           but an ORM model '''
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        '''Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
           but an ORM model '''
        orm_mode = True
