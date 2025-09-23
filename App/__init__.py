from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


from .db import init_db
from .routes.User_router import user_router
from .routes.Auth_route import auth_router
from .utils import limiter,RateLimitExceeded


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
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            'message':"Too many requests"
        }
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,rate_limit_exceeded_handler)

app.include_router(auth_router,prefix="/api/v0/auth",tags=['Auth'])
app.include_router(user_router,prefix="/api/v0/users",tags=['User'])

@app.get("/")
def check_helth(request: Request):
    return {'status':'Running'}




