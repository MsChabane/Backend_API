from fastapi import APIRouter ,status,HTTPException,Depends
from ..schemas import UserModel,NewUserModel,UserLogin,Token,Refreched_Token
from ..dependencies import db_dependency,get_current_user,refresh_token_dependency
from ..services.user_services import UserServices
from ..utils import checkpwd,create_token


auth_router = APIRouter()
user_services = UserServices()

@auth_router.post("/sign-up",response_model=UserModel, status_code=status.HTTP_200_OK)
async def sign_up(user_data:NewUserModel,session:db_dependency):
    if await user_services.check_user_exist(user_data.email,session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user is already exist.")
    
    user = await user_services.add(session=session,user_data=user_data)
    return user





@auth_router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
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



@auth_router.get("/me",response_model=UserModel)
def me(user= Depends(get_current_user)):
    return user



@auth_router.post("/refrech",response_model=Refreched_Token)
async def create_new_access_token(token_data:refresh_token_dependency ) :
    data = {"user_id":token_data.user_id}
    access_token= create_token(data,acces_token=True)
    return Refreched_Token(access_token=access_token)