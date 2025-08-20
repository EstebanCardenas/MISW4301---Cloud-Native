from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.http_server import router as post_router
from src.database.config import Base, engine
from src.exceptions.api_exception import ApiException, ApiExceptionType

Base.metadata.create_all(bind=engine)

app = FastAPI(title="posts-app")

API_EXCEPTION_STATUS_MAP = {
    ApiExceptionType.VALIDATION_FAILED: 412,
    ApiExceptionType.NOT_FOUND: 404,
    ApiExceptionType.INVALID_INPUT: 400,
}

PYDANTIC_EXCEPTION_STATUS_MAP: dict[str, int] = {"enum": 412}


@app.middleware("http")
async def api_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ApiException as exc:
        status_code = API_EXCEPTION_STATUS_MAP.get(exc.type, 500)
        return JSONResponse(
            status_code=status_code,
            content={"error_type": exc.type.value, "msg": exc.detail},
        )
    except Exception as exc:
        return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=PYDANTIC_EXCEPTION_STATUS_MAP.get(exc.errors()[0]["type"], 400),
        content={"msg": exc.errors()},
    )


app.include_router(post_router)
