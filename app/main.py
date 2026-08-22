
from dotenv import load_dotenv
load_dotenv()
import time
import logging

from app.routers.ask import router as ask_router
from fastapi import FastAPI
from app.api.chat import router as chat_router
from fastapi import Request
from fastapi.responses import JSONResponse
from app.routers.documents import router as documents_router

from app.core.exceptions import AIPlatformException
app = FastAPI()
logger = logging.getLogger("api")


@app.exception_handler(AIPlatformException)
async def exception_handler(
    request: Request,
    exc: AIPlatformException
):

    return JSONResponse(
        status_code=500,
        content={
            "error": exc.message
        }
    )
app.include_router(chat_router)

@app.get("/")
def home():
    return {
        "message": "AI Knowledge Platform Backend Running"
    }

@app.get("/health")
def health():
    return{
        "status":"healthy"
    }

@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {duration}s"
    )

    return response
app.include_router(documents_router)


app.include_router(ask_router)