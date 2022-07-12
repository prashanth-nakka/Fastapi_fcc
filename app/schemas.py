from typing import Optional
from pydantic import BaseModel
from .database import Base


# Schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # optional fileds
    # # rating: Optional[int] = None


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