import bcrypt
from jose import jwt,JWTError
from datetime import timedelta,datetime
from App.config import config

def hash(password:str)-> str:
    salt = bcrypt.gensalt()
    hashed=bcrypt.hashpw(password=password.encode(),salt=salt)
    return hashed.decode()


def checkpwd(password:str,hashed:str)-> bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())


def create_token(data:dict,acces_token:bool=True):
    expiry = timedelta(minutes=2) if acces_token else timedelta(days=7)
    data["exp"]=datetime.now()+expiry
    data['refresh']= not acces_token
    token = jwt.encode(data,config.JWT_SECRET)
    return token

def decode_token(token:str):
    try:
        token_data= jwt.decode(token,config.JWT_SECRET,algorithms=[config.JWT_ALGORITHME])
        return token_data
    except JWTError as e:
        return None


