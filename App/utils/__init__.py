import bcrypt
from jose import jwt,JWTError,ExpiredSignatureError
from datetime import timedelta,datetime,timezone
from App.config import config
from ..db import redis
import uuid
from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired
import logging
import colorlog

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

TOKEN_EXPIRY=300

serilizer = URLSafeTimedSerializer(secret_key=config.SERILIZER_SECRET)

def create_url_safe_token(data:dict)-> str:
    token= serilizer.dumps(obj=data)
    return token

def decode_url_safe_token(token:str,max_age:int=None)->dict:
    try:
         return serilizer.loads(token,max_age=max_age),0

    except BadSignature as e :
         return None ,1
    except SignatureExpired as e:
         return None,2

async def add_to_blocklist(token_id):
        await redis.set(name=token_id,value="",ex=TOKEN_EXPIRY)

async def isblocked(token_id)->bool:
     return (await redis.get(token_id) ) is not  None 

def hash(password:str)-> str:
    salt = bcrypt.gensalt()
    hashed=bcrypt.hashpw(password=password.encode(),salt=salt)
    return hashed.decode()




def checkpwd(password:str,hashed:str)-> bool:
    return bcrypt.checkpw(password.encode(),hashed.encode())


def create_token(data:dict,acces_token:bool=True):
    expiry = timedelta(minutes=2) if acces_token else timedelta(days=1)
    data["exp"]=int((datetime.now(timezone.utc)+expiry).timestamp())
    data["jti"]=str(uuid.uuid4())
    data['refresh']= not acces_token
    token = jwt.encode(data,config.JWT_SECRET)
    return token

def decode_token(token:str)->dict:
    try:
        token_data= jwt.decode(token,config.JWT_SECRET,algorithms=[config.JWT_ALGORITHME])
        return token_data,0
    except ExpiredSignatureError as e:
         return None,1
    except JWTError as e:
        return None,2


def get_logger(name:str)->logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  

    
    stream_handler = logging.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(levelname)-s:%(asctime)8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
        }
    )
    stream_handler.setFormatter(formatter)

    
    if logger.hasHandlers():
        logger.handlers.clear()

    
    logger.addHandler(stream_handler)
    return logger

