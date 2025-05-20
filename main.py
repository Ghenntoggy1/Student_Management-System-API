from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routers.user_router import user_router
from routers.auth_router import auth_router



app = FastAPI()

app.include_router(router=auth_router)
app.include_router(router=user_router)

