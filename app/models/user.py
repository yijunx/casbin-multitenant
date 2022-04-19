from re import S
from pydantic import BaseModel


class User(BaseModel):

    id: str
    name: str
    tenant_id: str

    # well we dont need other fields just for dmo

    class Config:
        orm_mode = True
