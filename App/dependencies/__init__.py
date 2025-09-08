from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status, Request
from typing import Annotated
from App.db import get_session
from fastapi.security import HTTPBearer
from ..utils import decode_token
from datetime import datetime
from ..models.User import User
from ..schemas import Token_Data


class Token_validator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Token_Data:
        creds = await super().__call__(request)
        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token."
            )

        token = creds.credentials
        token_data = decode_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token."
            )

        self.validate_token_data(token_data)
        print()
        return Token_Data(**token_data)

    def validate_token_data(self, token_data: dict):
        raise NotImplementedError()


class Access_Token_validator(Token_validator):
    def validate_token_data(self, token_data: dict):
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide an access token."
            )
        if datetime.now().timestamp() > token_data["exp"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token expired."
            )


class Refresh_Token_validator(Token_validator):
    def validate_token_data(self, token_data: dict):
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a refresh token."
            )
        if datetime.now().timestamp() > token_data["exp"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token expired."
            )


db_dependency = Annotated[AsyncSession, Depends(get_session)]
access_token_dependency = Annotated[Token_Data, Depends(Access_Token_validator())]
refresh_token_dependency = Annotated[Token_Data, Depends(Refresh_Token_validator())]


async def get_current_user(
    token_data: access_token_dependency,
    session: db_dependency
) -> User:
    print(token_data)
    user = await session.get(User, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user


current_user_dependency = Annotated[User, Depends(get_current_user)]
