import logging

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.exception_handlers import http_exception_handler
from sqlalchemy.exc import NoResultFound

from handsy.api.auth import JWTBearer
from handsy.api.db import create_db_engine, dispose_db_engine, db_session_manager
from handsy.api.db.exceptions import SelectFailed, UpdateFailed, DeleteFailed, CredentialsRequired
from handsy.api.endpoints.user import router as user_router
from handsy.api.endpoints.auth import router as auth_router
from handsy.api.endpoints.group import router as group_router
from handsy.api.endpoints.item import router as item_router
from handsy.api.endpoints.comment import router as comment_router

logger = logging.getLogger(__name__)

# init FastAPI and include routes
app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(item_router)
app.include_router(comment_router)


# when writing middleware, the last middleware function will be called first
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with db_session_manager() as session:
        request.state.db = session
        response = await call_next(request)
        del request.state.db
    return response


@app.exception_handler(NoResultFound)
async def no_result_found_exception_handler(request: Request, exc: NoResultFound):
    return await http_exception_handler(request, HTTPException(status_code=404, detail=str(exc)))


@app.exception_handler(SelectFailed)
async def select_failed_exception_handler(request: Request, exc: SelectFailed):
    return await http_exception_handler(request, HTTPException(status_code=404, detail=str(exc)))


@app.exception_handler(UpdateFailed)
async def update_failed_exception_handler(request: Request, exc: UpdateFailed):
    return await http_exception_handler(request, HTTPException(status_code=400, detail=str(exc)))


@app.exception_handler(DeleteFailed)
async def delete_failed_exception_handler(request: Request, exc: DeleteFailed):
    return await http_exception_handler(request, HTTPException(status_code=400, detail=str(exc)))


@app.exception_handler(CredentialsRequired)
async def missing_credentials_exception_handler(request: Request, exc: CredentialsRequired):
    return await http_exception_handler(request, HTTPException(status_code=400, detail=str(exc)))


async def root_app_startup():
    await create_db_engine()
    logger.info("Database engine created")


async def root_app_shutdown():
    await dispose_db_engine()
    logger.info("Database engine disposed")


@app.on_event("startup")
async def startup():
    await root_app_startup()
    logger.info("Root app started")


@app.on_event("shutdown")
async def shutdown():
    await root_app_shutdown()
    logger.info("Root app shutdown")
