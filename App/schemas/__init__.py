from pydantic import BaseModel
import uuid
from typing  import Optional

class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    email:str
    password: str


class UserModel(BaseModel):    
    id:str
    first_name: str
    last_name: str
    email:str
    is_verified: bool

class UpdateUser(BaseModel):
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    is_verified: Optional[bool]=None


