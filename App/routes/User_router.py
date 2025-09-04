from fastapi import APIRouter ,status,HTTPException
from ..schemas import UserModel,NewUserModel,UpdateUser
from ..dependencies import db_dependency
from typing import List,Optional
from ..services.user_services import UserServices


user_router = APIRouter()
user_services = UserServices()

@user_router.get("/",status_code=status.HTTP_200_OK,response_model=List[UserModel])
async def get_all_user(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    return await user_services.get_all(page=page,limit=limit,session=session)

@user_router.post("/",response_model=UserModel, status_code=status.HTTP_200_OK)
async def add_user(user_data:NewUserModel,session:db_dependency):
    user = await user_services.add(session=session,user_data=user_data)
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user is already exist.")
    return user



@user_router.get("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user_by_id(id:str,session:db_dependency):
    user = await user_services.get(user_id=id,session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.")
    return user

@user_router.put("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def update_user(id:str,user_data:UpdateUser,session:db_dependency):
    user = await user_services.update(user_id=id,user_data=user_data,session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.")
    return user

@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(id:str,session:db_dependency):
    user = await user_services.delete(user_id=id,session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user is not found.")
    return {}

    


