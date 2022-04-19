from pydantic import BaseModel


class Item(BaseModel):

    id: str
    name: str
    content: str
    created_by: str

    class Config:
        orm_mode = True
