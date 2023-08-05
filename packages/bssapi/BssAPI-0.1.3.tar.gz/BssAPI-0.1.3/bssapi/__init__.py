__version__ = '0.1.3'
__all__ = [r'api', r'app']

import uvicorn
import fastapi.middleware
import fastapi.middleware.gzip
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, UJSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .api.router import router

api = fastapi.FastAPI(debug=False, version=__version__,
                      middleware=[
                          fastapi.middleware.Middleware(fastapi.middleware.gzip.GZipMiddleware, minimum_size=100)],
                      openapi_tags=[
                          {
                              "name": "DBF",
                              "description": "Операции с файлами DBF"
                          }
                      ],
                      docs_url="/test", redoc_url="/",
                      title="BssAPI", description="Функционал перефирийного взаимодействия "
                                                  "корпоративной учетной системы BSS",
                      default_response_class=UJSONResponse,
                      routes=router.routes)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        content={
                            "detail": jsonable_encoder(exc.errors()),
                            "body": jsonable_encoder(exc.body) if exc.body else None
                        })


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        content={
                            "detail": jsonable_encoder(exc.errors()),
                            "body": jsonable_encoder(exc.body) if exc.body else None
                        })


async def type_error_exception_handler(request: Request, exc: TypeError) -> JSONResponse:
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                        content={"detail": str(exc)})


api.add_exception_handler(RequestValidationError, request_validation_exception_handler)
api.add_exception_handler(ValidationError, validation_exception_handler)
api.add_exception_handler(TypeError, type_error_exception_handler)

app = uvicorn.Server(
    uvicorn.Config(app='bssapi:api', debug=api.debug, limit_max_requests=10000,
                   host="0.0.0.0", use_colors=True, proxy_headers=False)).run
