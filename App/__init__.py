from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import init_db
from .dependencies import db_dependency
from .models.heros import Hero
from sqlmodel import select



@asynccontextmanager
async def lifespan(app:FastAPI):
    print("starting")
    await init_db()
    yield
    print("stopping")


app = FastAPI(
    title='backend',
    lifespan=lifespan
)



@app.get("/")
def check_helth():
    return {'status':'Running'}


@app.get("/get")
async def d(session:db_dependency) :  # type: ignore
    result = await session.execute(select(Hero))
    return result.scalars().all()





