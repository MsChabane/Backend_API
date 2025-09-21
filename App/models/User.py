


from sqlmodel import SQLModel ,Field
import uuid
from datetime import datetime,date

class User (SQLModel,table =True):
    __tablename__='users'

    id:str = Field(primary_key=True,default_factory =lambda: str(uuid.uuid4()),index=True)
    first_name: str 
    last_name : str
    email :str = Field(unique=True,nullable=False,max_length=40,index=True)
    password:str =Field(exclude=True)
    is_verified :bool =Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=  datetime.now)


