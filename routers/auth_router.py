from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from schemas.schemas import GenericResponse, UserLogin, Token
from services import service
from db.db import get_database_session
import auth.auth as auth_layer

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post(path="/login/",
          response_model=Token)
async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_database_session)):
    user_obj = service.get_user_by_email(email=user.username, db=db)
    if not user_obj or not auth_layer.verify_password(user.password, user_obj.Password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )

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
    # return response
    return Token(access_token=access_token, token_type="bearer")
