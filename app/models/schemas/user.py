from pydantic import BaseModel
from typing import List, Optional


class UserInJWT(BaseModel):
    id: str
    email: str
    name: str
    user_name: Optional[str]
    tenant_id: Optional[str]
    roles: Optional[List[str]]  # they are role names
