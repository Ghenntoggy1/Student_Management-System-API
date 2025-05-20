from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from enums.db_enums import RolesEnum
from schemas.schemas import GenericResponse, UserResponse, UserRequest, TokenData
from services import service
from db.db import get_database_session
from services.service import jwt_validation_response

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# C - Create Operations
# Add User Entity.
@user_router.post("/add_user/", response_model=GenericResponse[UserResponse])
async def add_user(user: UserRequest, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
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
@user_router.get("/", response_model=GenericResponse[list[UserResponse]])
async def get_all_users(jwt_token: TokenData = Depends(jwt_validation_response), skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
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
@user_router.get("/id={user_id}", response_model=GenericResponse[UserResponse])
async def get_user_by_id(user_id: int, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )

    user = service.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

# Get User by Email
@user_router.get("/email={email}", response_model=GenericResponse[UserResponse])
async def get_user_by_email(email: str, jwt_token: TokenData = Depends(jwt_validation_response), db: Session = Depends(get_database_session)):
    jwt_token_role: RolesEnum = jwt_token.role
    if RolesEnum.admin != jwt_token_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have required permission to perform this action.",
            headers = {
                "WWW-Authenticate": "Bearer"
            },
        )

    user = service.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    response = GenericResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=user
    )
    return response

