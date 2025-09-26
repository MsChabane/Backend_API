from fastapi import APIRouter ,status
from ..schemas import UserModel,UpdateUser
from ..dependencies import db_dependency
from typing import List,Optional
from ..services.user_services import UserServices
from ..errors import UserNotFound


user_router = APIRouter()
user_services = UserServices()


@user_router.get("/",status_code=status.HTTP_200_OK,response_model=List[UserModel])
async def get_all_user(session:db_dependency,page:Optional[int]=1,limit:Optional[int]=10):
    return await user_services.get_all(page=page,limit=limit,session=session)


@user_router.get("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def get_user_by_id(id:str,session:db_dependency):
    user = await user_services.get(user_id=id,session=session)
    if user is None:
        raise UserNotFound()
    return user

@user_router.patch("/{id}",response_model=UserModel, status_code=status.HTTP_200_OK)
async def update_user(id:str,user_data:UpdateUser,session:db_dependency):
    user =await user_services.get(id,session)
    if user is None :
        raise UserNotFound()
    user = await user_services.update(user=user,user_data=user_data,session=session)
    return user

@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def detete_user(id:str,session:db_dependency):
    user= await user_services.get(id,session) 
    if user is None:
        raise UserNotFound()
    await user_services.delete(user=user,session=session)
    return {}

    






    
    


