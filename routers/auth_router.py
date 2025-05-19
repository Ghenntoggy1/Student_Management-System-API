from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.schemas import GenericResponse, UserLogin
from services import service
from db.db import get_database_session
import auth.auth as auth_layer

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post(path="/login/",
          response_model=GenericResponse)
async def login(user: UserLogin, db: Session = Depends(get_database_session)):
    user_obj = service.get_user_by_email(email=user.email, db=db)
    if not user_obj or not auth_layer.verify_password(user.password, user_obj.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials.")

    access_token = auth_layer.create_access_token(
        data={
            "sub": user_obj.Email,
            "name": user_obj.FirstName + " " + user_obj.LastName,
            "role": user_obj.Role,
        }
    )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Login successful. Token is issued",
        data={
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
    return response

