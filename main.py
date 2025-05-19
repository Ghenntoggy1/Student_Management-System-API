from fastapi import FastAPI

from routers.user_router import user_router
from routers.auth_router import auth_router


app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=user_router)

