from pydantic import BaseModel


class ItemCreate(BaseModel):

    name: str
    content: str
