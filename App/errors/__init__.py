from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from typing import Callable
from ..utils import get_logger
import traceback

from ..schemas import Error

class AppException(Exception):
    pass
class UserNotFound(AppException):
    pass
class UserExist(AppException):
    pass
class TokenRequired(AppException):
    pass
class TokenExpired(AppException):
    pass
class TokenInvalid(AppException):
    pass
class AccessTokenInvalid(AppException):
    pass
class AccessTokenExpired(AppException):
    pass
class AccessTokenRevoked(AppException):
    pass
class AccessTokenRequired(AppException):
    pass
class RefreshTokenRequired(AppException):
    pass
class RefreshTokenInvalid(AppException):
    pass
class RefreshTokenExpired(AppException):
    pass
class UserNotVerified(AppException):
    pass
class UserVerified(AppException):
    pass
class InvalidPassword(AppException):
    pass

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = {}
    for err in exc.errors():
        loc = ".".join([str(x) for x in err["loc"] if x not in ("body",)]) 
        error_details[loc] = err["msg"]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=Error(
            error="unprocessable entity",
            code="validation_error",
            details=error_details  
        ).model_dump()
    )
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            'message':"Too many requests"
        }
    )

def create_exception_handler(status_code:int,detail:Error)->Callable[[Request,AppException],JSONResponse]:
    async def exception_handler(request:Request,exc:AppException)->JSONResponse:
        return JSONResponse(
            content=detail.model_dump(),
            status_code=status_code
        )
    return exception_handler
    
def register_exceptions_handler(app:FastAPI):
    app.add_exception_handler(UserNotFound,create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=Error(
            error="user is not found.",
            code='user_not_found'
        )
    ))
    app.add_exception_handler(UserExist,create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=Error(
            error="user is already exist.",
            code='user_exist'
        )
    ))
    app.add_exception_handler(InvalidPassword,create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=Error(
            error="invalid password ",
            code='invalid_password',
            details={
                "password":'wrong password'
            }
        )
    ))
    app.add_exception_handler(UserNotVerified,create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=Error(
            error="account is not verified.",
            code='user_not_active'
        )
    ))
    app.add_exception_handler(UserVerified,create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=Error(
            error="account is  verified.",
            code='user_active'
        )
    ))
    app.add_exception_handler(AccessTokenInvalid,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="access token is not valid",
            code='access_token_invalid'
        )
    ))
    app.add_exception_handler(AccessTokenExpired,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="access token is expired",
            code='access_token_expired'
        )
    ))
    app.add_exception_handler(AccessTokenRequired,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="access token is required",
            code='access_token_required'
        )
    ))
    app.add_exception_handler(TokenRequired,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="token is required",
            code='token_required'
        )
    ))
    app.add_exception_handler(TokenExpired,create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=Error(
            error="token is expired",
            code='token_expired'
        )
    ))
    app.add_exception_handler(TokenInvalid,create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=Error(
            error="token is invalid",
            code='token_invalide'
        )
    ))
    
    app.add_exception_handler(AccessTokenRevoked,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="access token is revoked",
            code='access_token_revoked'
        )
    ))


    app.add_exception_handler(RefreshTokenInvalid,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="refresh token is not valid",
            code='refresh_token_invalid'
        )
    ))
    app.add_exception_handler(RefreshTokenExpired,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="refresh token is expired",
            code='refresh_token_expired'
        )
    ))
    app.add_exception_handler(RefreshTokenRequired,create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Error(
            error="refresh token is required",
            code='refresh_token_required'
        )
    ))
    app.add_exception_handler(RequestValidationError,validation_exception_handler)
    app.add_exception_handler(RateLimitExceeded,rate_limit_exceeded_handler)
    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        logger = get_logger("logger")
        logger.error(
            "Internal server error: %s\n%s",
            exc,
            traceback.format_exc()
        )

        
        return JSONResponse(
            status_code=500,
            content=Error(
                code="internal_server_error",
                error="Something went wrong on our side. Please try again later."
            ).model_dump()
        )
    


from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # ensure components.schemas exists
    openapi_schema.setdefault("components", {}).setdefault("schemas", {})
    openapi_schema["components"]["schemas"]["Error"] = Error.model_json_schema()

    # loop through all paths
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            responses = details.get("responses", {})
            for status_code, response in responses.items():
                if status_code != "200":
                    content = response.get("content", {})
                    if "application/json" in content:
                        content["application/json"]["schema"] = {
                            "$ref": "#/components/schemas/Error"
                        }

    app.openapi_schema = openapi_schema
    return app.openapi_schema