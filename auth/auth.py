from email.policy import default

import jwt
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, timezone, datetime
from enums.enums import RolesEnum

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRY_TIME_MINUTES = float(os.getenv("JWT_EXPIRY_TIME_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRY_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    # try:
    #     decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    #     return decoded_token
    # except jwt.ExpiredSignatureError:
    #     return {"error": "Token has expired"}
    # except jwt.InvalidTokenError:
    #     return {"error": "Invalid token"}

    decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return decoded_token

def verify_password(plain_password, hashed_password):
    return hashed_password == plain_password