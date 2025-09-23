from pydantic import BaseModel,EmailStr
from typing  import Optional,Literal
from datetime import timedelta
class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    email:EmailStr
    password: str


class UserModel(BaseModel):    
    id:str
    first_name: str
    last_name: str
    email:EmailStr
    is_verified: bool

class UpdateUser(BaseModel):
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    is_verified: Optional[bool]=None


class UserLogin(BaseModel):
    email:EmailStr
    password :str

class Refreched_Token(BaseModel):
    access_token:str
    token_type:Literal['Bearer']='Bearer'


class Token(Refreched_Token):
    refresh_token:str

class Token_Data(BaseModel):
    user_id:str
    refresh:bool
    exp:timedelta
    jti:str

class Verfication(BaseModel):
    message:str

