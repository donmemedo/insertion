"""_summary_
"""
import asyncio
import datetime
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from khayyam import JalaliDatetime as jd

from src.routers.faq import faq_router
from src.routers.forbidden import forbidden_router
from src.routers.professional import professional_router
from src.routers.sensitive import sensitive_router
from src.routers.tags import tags_router
from src.routers.searches import search_router
from src.utils.config import settings
from src.utils.database import get_database
from src.utils.errors import get_error
from src.utils.logger import logger

app = FastAPI(
    version=settings.VERSION,
    title=settings.SWAGGER_TITLE,
    docs_url=settings.FASTAPI_DOCS,
    redoc_url=settings.FASTAPI_REDOC,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts = settings.ORIGINS.split(","),
# )


@app.on_event("startup")
async def startup_events():
    logger.info(f"Time of Startup:{jd.now().isoformat()}")
    get_database()
    # token = await get_token()
    # await set_permissions(permissions, token)
    logger.info(f"Ready for Your Insertions:{jd.now().isoformat()}")
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())


async def periodic():
    while True:
        db = get_database()
        try:
            db.dbhealthcheck.insert_one({"Time": datetime.datetime.now().isoformat()})
            logger.info(
                f"Database Connection is OK in {datetime.datetime.now().isoformat()}"
            )
        except:
            logger.critical(
                f"Database Connection is FAILED in {datetime.datetime.now().isoformat()}"
            )

        await asyncio.sleep(300)


@app.get("/health-check", tags=["Deafult"])
def health_check():
    logger.info("Status of Insertion Service is OK")
    return {"status": "OK"}


@app.get("/ip-getter", tags=["Deafult"])
async def read_root(request: Request):
    client_host = request.client.host
    client_scope = request.scope["client"]
    logger.info(f"client host is {client_host}")
    logger.info(f"client scope is {client_scope}")

    return {"client_host": client_host, "client_scope": client_scope}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    status = 400
    try:
        err = get_error(exc.errors().__name__, exc.body["code"])
        status = exc.body["status"]
    except:
        for e in exc.errors():
            try:
                err = get_error(e["type"], e["ctx"]["error"])
                status = err["code"]
            except:
                err = get_error(e["type"], e["msg"])
                status = err["code"]
    response = {
        "result": [],
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": err,
    }
    logger.error(exc)
    return JSONResponse(status_code=status, content=response)


# Add all routers
app.include_router(tags_router, prefix="")
app.include_router(sensitive_router, prefix="")
app.include_router(professional_router, prefix="")
app.include_router(forbidden_router, prefix="")
app.include_router(faq_router, prefix="")
app.include_router(search_router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=80)#, log_config=dictConfig(logger))
