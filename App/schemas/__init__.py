from pydantic import BaseModel,EmailStr,Field
from typing  import Optional,Literal
from datetime import timedelta
class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    email:EmailStr=Field(max_length=40)
    password: str


class UserModel(BaseModel):    
    id:str
    first_name: str
    last_name: str
    email:EmailStr=Field(max_length=40)
    is_verified: bool

class UpdateUser(BaseModel):
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    


class UserLogin(BaseModel):
    email:EmailStr=Field(max_length=40)
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

class Message(BaseModel):
    message:str

class Reset_password(BaseModel):
    email:EmailStr=Field(max_length=40)
    new_password:str
