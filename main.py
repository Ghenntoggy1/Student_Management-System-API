from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers.course_router import course_router
from routers.user_router import user_router
from routers.auth_router import auth_router
from routers.session_router import session_router
from routers.attendance_router import attendance_router
from schemas.schemas import GenericResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=GenericResponse(
            status_code=exc.status_code,
            message=exc.detail,
            data={}
        ).model_dump()
    )

app.include_router(router=auth_router)
app.include_router(router=user_router)
app.include_router(router=course_router)
app.include_router(router=session_router)
app.include_router(router=attendance_router)
