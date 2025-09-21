from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import init_db
from .routes.User_router import user_router
from .routes.Auth_route import auth_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("starting")
    await init_db()
    yield
    print("stopping")


app = FastAPI(
    title='backend',
    lifespan=lifespan,
    version="0.0.1"
)

app.include_router(auth_router,prefix="/api/v0/auth",tags=['Auth'])
app.include_router(user_router,prefix="/api/v0/users",tags=['User'])

@app.get("/")
def check_helth():
    return {'status':'Running'}




