from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status, Request
from typing import Annotated
from App.db import get_session
from fastapi.security import HTTPBearer
from ..utils import decode_token,isblocked
from ..models.User import User
from ..schemas import Token_Data
from ..errors import (AccessTokenRequired,AccessTokenExpired,
                      AccessTokenInvalid,AccessTokenRevoked,TokenRequired,
                      RefreshTokenExpired,RefreshTokenInvalid,RefreshTokenRequired,
                      UserNotFound
)

class TokenChecker(HTTPBearer):
    def __init__(self):
         super().__init__(auto_error=False)

    async def __call__(self, request: Request) -> Token_Data:
        creds = await super().__call__(request)
        if creds is None:
            raise TokenRequired()
        token = creds.credentials
        token_data,token_status = decode_token(token)

        await self.check(token_data,token_status)
        
        return Token_Data(**token_data)

    async def check(self, token_data: dict,token_status:int):
        raise NotImplementedError()


class AccessTokenChecker(TokenChecker):
    async def check(self, token_data: dict,token_status:int):
        if token_status == 1:
            raise AccessTokenExpired()
        
        if token_status == 2:
            raise AccessTokenInvalid()
        if token_data.get("refresh", False):
            raise AccessTokenRequired()
        if await isblocked(token_id=token_data.get("jti")):
            raise AccessTokenRevoked()
        

class RefreshTokenChecker(TokenChecker):
    async def check(self, token_data: dict,token_status):
        if token_status == 1:
            raise RefreshTokenExpired()
        if token_status == 2:
            raise RefreshTokenInvalid()
        if not token_data.get("refresh", False):
            raise RefreshTokenRequired()


db_dependency = Annotated[AsyncSession, Depends(get_session)]
access_token_dependency = Annotated[Token_Data, Depends(AccessTokenChecker())]
refresh_token_dependency = Annotated[Token_Data, Depends(RefreshTokenChecker())]





async def get_current_user(
    token_data: access_token_dependency,
    session: db_dependency
) -> User:

    user = await session.get(User, token_data.user_id)
    if not user:
        raise UserNotFound()
    return user





