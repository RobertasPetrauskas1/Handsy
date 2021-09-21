from fastapi import FastAPI
import os
from handsy.api.endpoints.user import router as user_router
from handsy.api.endpoints.auth import router as auth_router
from handsy.api.endpoints.group import router as group_router
from handsy.api.endpoints.item import router as item_router
from handsy.api.endpoints.comment import router as comment_router

# load env variables
port = os.environ.get("PORT")

# init FastAPI and include routes
app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(group_router)
app.include_router(item_router)
app.include_router(comment_router)

