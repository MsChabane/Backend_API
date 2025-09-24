from fastapi import APIRouter ,status,HTTPException,Depends,BackgroundTasks,Request
from ..schemas import UserModel,NewUserModel,UserLogin,Token,Refreched_Token,UpdateUser,Message,Reset_password
from ..dependencies import db_dependency,get_current_user,refresh_token_dependency,access_token_dependency
from ..services.user_services import UserServices
from ..utils import checkpwd,create_token,create_url_safe_token,decode_url_safe_token,add_to_blocklist
from ..mail import send_verifcation_mail,send_reset_password
from pydantic import EmailStr
from ..utils import limiter


auth_router = APIRouter()
user_services = UserServices()


@auth_router.post("/sign-up",response_model=UserModel, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def sign_up(user_data:NewUserModel,session:db_dependency,task:BackgroundTasks, request: Request ):
    if await user_services.check_user_exist(user_data.email,session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user is already exist.")
    
    user = await user_services.add(session=session,user_data=user_data)
    
    token = create_url_safe_token({"email":user.email})
    link=f"{str(request.base_url).rstrip("/") }/api/v0/auth/verify/{token}"
    task.add_task(send_verifcation_mail,email=user.email,link=link)
    return user




@auth_router.post("/login",response_model=Token,status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(login_data:UserLogin,session: db_dependency,request:Request):
    
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
@limiter.limit("5/minute")
def me(request:Request,user= Depends(get_current_user)):
    return user

@auth_router.post('/send-verifcation-token',response_model=Message)
@limiter.limit("3/1hour")
async def send_verifaction_token(email:EmailStr,session:db_dependency,task :BackgroundTasks,request:Request):
    user =await user_services.get_by_email(email=email,session=session)
    if user is None :
        raise  HTTPException(
            detail="User is not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    if user.is_verified :
        raise  HTTPException(
            detail="User is verified",
            status_code=status.HTTP_403_FORBIDDEN
        )
    token = create_url_safe_token({"email":user.email})
    link=f"{str(request.base_url).rstrip("/") }/api/v0/auth/verify/{token}"
    task.add_task(send_verifcation_mail,email=user.email,link=link)
    
    return Message( message='verification token is send successfelly')



@auth_router.post("/verify/{token}",response_model=Message)
async def verify(token:str,session:db_dependency):
    data,token_status = decode_url_safe_token(token)
    
    if token_status== 1:
        raise HTTPException(
            detail="Invalid token .",
            status_code=status.HTTP_403_FORBIDDEN
        )
    if token_status== 2:
        raise HTTPException(
            detail="Token has been Expired .",
            status_code=status.HTTP_403_FORBIDDEN
        )
    email = data.get("email",None)
    user = await user_services.get_by_email(email,session)
    if user is None :
        raise  HTTPException(
            detail="User is not found ",
            status_code=status.HTTP_404_NOT_FOUND
        )
    user=await user_services.activate(user=user,session=session)
    if user is None:
        raise HTTPException(
            detail="Can't verify the user",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return Message( message='verification is done successefelly')

@auth_router.post('/send-reset-password-token',response_model=Message)
@limiter.limit("3/1hour")
async def send_reset_password_token(email:EmailStr,session:db_dependency,task :BackgroundTasks,request:Request):
    user =await user_services.get_by_email(email=email,session=session)
    if user is None :
        raise  HTTPException(
            detail="User is not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    token = create_url_safe_token({"email":user.email})

    task.add_task(send_reset_password,email=user.email,token=token)
    
    return Message( message='token has been send .')


@auth_router.post("/reset-password/{token}",response_model=Message)
async def verify(token:str,reset_password_data:Reset_password,session:db_dependency):
    data,token_status = decode_url_safe_token(token,max_age=1800)
    if token_status== 1:
        raise HTTPException(
            detail="Invalid token .",
            status_code=status.HTTP_403_FORBIDDEN
        )
    if token_status== 2:
        raise HTTPException(
            detail="Token has been Expired .",
            status_code=status.HTTP_403_FORBIDDEN
        )
    email = data.get("email",None)
    if email != reset_password_data.email :
        raise HTTPException(
            detail="Emails not match",
            status_code=status.HTTP_403_FORBIDDEN
        )
    user = await user_services.get_by_email(email,session)
    if user is None :
        raise  HTTPException(
            detail="User is not found ",
            status_code=status.HTTP_404_NOT_FOUND
        )
    user=await user_services.change_password(user=user,new_password=reset_password_data.new_password,session=session)
    if user is None:
        raise HTTPException(
            detail="Can't verify the user",
            status_code=status.HTTP_403_FORBIDDEN
        )
    return Message( message='Password has been changed successfelly.')


@auth_router.post("/refrech",response_model=Refreched_Token)
@limiter.limit("5/minute")
async def create_new_access_token(token_data:refresh_token_dependency ,request:Request) :
    data = {"user_id":token_data.user_id}
    access_token= create_token(data,acces_token=True)
    return Refreched_Token(access_token=access_token)

@auth_router.post("/logout",response_model=Message)
async def logout(token_data:access_token_dependency):
    jti= token_data.jti
    await add_to_blocklist(jti)
    return Message(
        message='logout successfelly'
    ) 
    

    