import bcrypt
import jwt
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, timezone, datetime
from enums.server_enums import JWTValidationResultsEnum
from schemas.schemas import TokenData

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRY_TIME_MINUTES = float(os.getenv("JWT_EXPIRY_TIME_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/", auto_error=False)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        issue_time = datetime.now(timezone.utc)
        expire = issue_time + expires_delta
    else:
        issue_time = datetime.now(timezone.utc)
        expire = issue_time + timedelta(minutes=JWT_EXPIRY_TIME_MINUTES)
    to_encode.update({"iat": issue_time, "exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode,
                             key=JWT_SECRET_KEY,
                             algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(jwt=token,
                                   key=JWT_SECRET_KEY,
                                   algorithms=[JWT_ALGORITHM])
        return TokenData(**decoded_token)
    except jwt.ExpiredSignatureError:
        return JWTValidationResultsEnum.is_expired
    except jwt.InvalidSignatureError:
        return JWTValidationResultsEnum.invalid_signature
    except jwt.InvalidTokenError:
        return JWTValidationResultsEnum.is_invalid
    except Exception as e:
        return "UNKNOWN_ERROR"

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))