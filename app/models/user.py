from typing import Optional, List
from pydantic import BaseModel
from app.models.pagination import ResponsePagination


class User(BaseModel):

    id: str
    name: str
    tenant_id: str

    # well we dont need other fields just for dmo

    class Config:
        orm_mode = True


class UserAsSharee(BaseModel):
    id: str
    name: str
    tenant_id: str
    role: Optional[str]


class UserAsShareeWithPaging(BaseModel):
    data: List[UserAsSharee]
    paging: ResponsePagination
