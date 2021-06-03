from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app import settings
from app.api.v1 import api_v1_router


def create_app() -> FastAPI:
    app = FastAPI(title='simple-payment-service')

    @app.exception_handler(AuthJWTException)
    def auth_exception_handler(_request: Request, exc: AuthJWTException):
        return JSONResponse(
            {'detail': exc.message},
            status_code=exc.status_code,
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(_request: Request, exc: HTTPException):
        return JSONResponse(
            {'detail': exc.detail},
            status_code=exc.status_code,
        )

    AuthJWT._secret_key = settings.AUTH_SECRET_KEY
    app.include_router(
        api_v1_router,
        prefix='/api/v1',
    )
    return app
