import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse

from src.api import router
from src.metadata import DESCRIPTION, TAG_METADATA, TITLE, VERSION
from src.schemas.response import BaseErrorResponse


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
        )
    else:
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None,
        )

    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fast_api_app()


@app.exception_handler(HTTPException)
def http_exc_handler(_: Request, exc: HTTPException) -> ORJSONResponse:
    payload = BaseErrorResponse(
        status=exc.status_code,
        details=exc.detail,
    ).model_dump()
    return ORJSONResponse(
        status_code=exc.status_code,
        content=payload,
    )
