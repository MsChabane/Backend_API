from fastapi import APIRouter ,status,HTTPException,Depends
from ..schemas import UserModel,NewUserModel,UpdateUser,UserLogin,Token
from ..dependencies import db_dependency,get_current_user,access_token_dependency
from typing import List,Optional
from ..services.user_services import UserServices
from ..utils import checkpwd,create_token


user_router = APIRouter()
user_services = UserServices()

@user_router.get("/",status_code=status.HTTP_200_OK,response_model=List[UserModel])
async def get_all_user(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    return await user_services.get_all(page=page,limit=limit,session=session)

@user_router.post("/",response_model=UserModel, status_code=status.HTTP_200_OK)
async def add_user(user_data:NewUserModel,session:db_dependency):
    if await user_services.check_user_exist(user_data.email,session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user is already exist.")
    
    user = await user_services.add(session=session,user_data=user_data)
    return user

@user_router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
async def login(login_data:UserLogin,session: db_dependency):
    
    user =await  user_services.get_by_email(login_data.email,session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.") 
    if not checkpwd(password=login_data.password,hashed=user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalide password.") 
    data = {"user_id":user.id}
    access_token= create_token(data,acces_token=True)
    refresh_token= create_token(data,acces_token=False)
    return Token(access_token=access_token,refresh_token=refresh_token)


@user_router.get("/me",response_model=UserModel)
def me(user= Depends(get_current_user)):
    return user


@user_router.get("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user_by_id(id:str,session:db_dependency):
    user = await user_services.get(user_id=id,session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.")
    return user

@user_router.patch("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def update_user(id:str,user_data:UpdateUser,session:db_dependency):
    user =await user_services.get(id,session)
    if user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.") 
    user = await user_services.update(user=user,user_data=user_data,session=session)
    return user

@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def detete_user(id:str,session:db_dependency):
    user= await user_services.get(id,session) 
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.") 
    await user_services.delete(user=user,session=session)
    return {}

    






    
    


