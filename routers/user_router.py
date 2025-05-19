from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from enums.db_enums import RolesEnum
from schemas.schemas import GenericResponse, UserResponse, Token, UserRequest
from services import service
from db.db import get_database_session

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# C - Create Operations
# Add User Entity.
@user_router.post("/add_user/", response_model=GenericResponse[UserResponse])
async def add_user(user: UserRequest, jwt_token: Token, db: Session = Depends(get_database_session)):
    decoded_token = service.jwt_validation_response(jwt_token)
    jwt_token_role: RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )
    db_user = service.add_user(db=db, user=user)
    response = GenericResponse(
        status_code=status.HTTP_201_CREATED,
        message="User added successfully.",
        data=db_user
    )
    return response


# R - Read Operations
# Get all Users.
@user_router.get("/users/", response_model=GenericResponse[list[UserResponse]])
async def get_all_users(jwt_token: Token, skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    decoded_token = service.jwt_validation_response(jwt_token)
    jwt_token_role: RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )

    users = service.get_all_users(skip=skip, limit=limit, db=db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="Users retrieved successfully",
        data=users
    )
    return response

# Get User by UserID
@user_router.get("/users/id={user_id}", response_model=GenericResponse[UserResponse])
async def get_user_by_id(jwt_token:Token, user_id: int, db: Session = Depends(get_database_session)):
    decoded_token = service.jwt_validation_response(jwt_token)
    jwt_token_role: RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )

    user = service.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

# Get User by Email
@user_router.get("/users/email={email}", response_model=GenericResponse[UserResponse])
async def get_user_by_email(email: str, jwt_token: Token, db: Session = Depends(get_database_session)):
    decoded_token = service.jwt_validation_response(jwt_token)
    jwt_token_role: RolesEnum = decoded_token.get("role")
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action."
        )

    user = service.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

