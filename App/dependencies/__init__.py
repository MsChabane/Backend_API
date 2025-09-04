from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from typing  import Annotated
from App.db import get_session


db_dependency = Annotated[AsyncSession,Depends(get_session)]
