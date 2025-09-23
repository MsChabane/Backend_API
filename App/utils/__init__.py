import bcrypt
from jose import jwt,JWTError,ExpiredSignatureError
from datetime import timedelta,datetime,timezone
from App.config import config
from ..db import redis
import uuid
from itsdangerous import URLSafeTimedSerializer,BadSignature

TOKEN_EXPIRY=300

serilizer = URLSafeTimedSerializer(secret_key=config.SERILIZER_SECRET)

def create_url_safe_token(data:dict)-> str:
    token= serilizer.dumps(obj=data)
    return token

def decode_url_safe_token(token:str)->dict:
    try:
         return serilizer.loads(token)
    except BadSignature as e :
         return None 

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
    expiry = timedelta(minutes=2) if acces_token else timedelta(days=7)
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


