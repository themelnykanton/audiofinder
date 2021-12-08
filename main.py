import time
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
from API.routers import file, auth, settings

app = FastAPI(redoc_url=None)

"""подключаем все роутеры апи"""
app.include_router(file.router)
app.include_router(auth.router)
app.include_router(settings.router)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    if request.scope['headers'][2][0] == 'x-real-ip' and len(request.scope['headers'][2]) >= 2:
        response.headers["IP"] = str(request.scope['headers'][2][1])

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    обрабатывает ошибки неправильно формата входящих на апи данных
    возвращает где и что было неправильно
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/")
def read_root(request: Request):
    return True
