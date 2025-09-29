from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from .config import config
from .routes.User_router import user_router
from .routes.Auth_route import auth_router
from .utils import limiter,get_logger,override_openapi
from .errors import register_exceptions_handler
import logging
import time


logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn.error").disabled = True

logger =get_logger("logger")





app = FastAPI(
    title='backend',
    version="0.0.1"
)


app.add_middleware(CORSMiddleware,
        allow_origins=config.ALLOWED_ORIGINS,
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=False
            )


@app.middleware("http")
async def middleware(request:Request,call_next):
    start = time.time()
    responce = await call_next(request)
    process_time=time.time()-start
    message=f" {request.method} - {request.url.path } -> {responce.status_code} | {process_time:.2f}s"
    if responce.status_code!=200:
        logger.error(message)
    else:
        logger.info(message)
    return responce
    


app.state.limiter = limiter


register_exceptions_handler(app=app)

app.include_router(auth_router,prefix="/api/v1/auth",tags=['Auth'])
app.include_router(user_router,prefix="/api/v1/users",tags=['User'])

@app.get("/")
def check_helth(request: Request):
    
    return {'status':'Running'}

app.openapi = lambda: override_openapi(app)



