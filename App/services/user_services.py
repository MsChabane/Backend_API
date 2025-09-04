from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.User import User
from ..schemas import NewUserModel,UpdateUser
from ..utils import hash


class UserServices:
    async def get_all(self,session:AsyncSession,page:int=1,limit:int=100):
        statement = select(User).offset((page-1)*limit ).limit(limit)
        result = await session.exec(statement)
        return result.all()
    

    async def get_by_email(self,email:str,session:AsyncSession):
        statement = select(User).where(User.email == email)
        user = (await session.exec(statement)).first()
        return user 
        

    async def check_user_exist(self,email:str,session:AsyncSession):
        return (await self.get_by_email(email,session)) is not None


    async def get(self,user_id:str,session:AsyncSession):
        user = await session.get(User, user_id)
        return user


    async def add( self,user_data:NewUserModel,session:AsyncSession):
        is_exist = await self.check_user_exist(user_data.email,session)
        if is_exist:
            return None
        user_data.password=hash(user_data.password)
        user =User(**(user_data.model_dump()))
        
        session.add(user)
        await session.commit()
        return user


    async def update(self,user_id:str,user_data:UpdateUser,session:AsyncSession):
        user =await self.get(user_id,session)
        if user is None :
            return 
        for k,v in user_data.model_dump(exclude_unset=True).items():
            setattr(user, k, v)
        session.add(user)
        await session.commit()
        return user
        
    async def delete(self,user_id,session:AsyncSession):
        user= await self.get(user_id,session) 
        if user is None:
            return None
        await session.delete(user)
        await session.commit()
        return user


