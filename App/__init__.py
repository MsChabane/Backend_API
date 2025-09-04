from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import init_db
from .routes.User_router import user_router



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

app.include_router(user_router,prefix="/api/users",tags=['User'])

@app.get("/")
def check_helth():
    return {'status':'Running'}




