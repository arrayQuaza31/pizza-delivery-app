from passlib.context import CryptContext
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timezone, timedelta
import uuid

from config_loader import Config


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(pwd: str) -> str:
    pwd_hash = PWD_CONTEXT.hash(pwd)
    return pwd_hash


def verify_password(pwd: str, hash: str) -> bool:
    return PWD_CONTEXT.verify(pwd, hash)


def create_token(user_data: dict, refresh_token_flag: bool = False) -> str:
    payload = {}
    payload["sub"] = user_data
    payload["exp"] = int(
        (
            datetime.now(timezone.utc)
            + (
                timedelta(minutes=Config.ACCESS_TOKEN_EXP)
                if not refresh_token_flag
                else timedelta(hours=Config.REFRESH_TOKEN_EXP)
            )
        ).timestamp()
    )
    payload["jti"] = str(uuid.uuid4())
    payload["is_refresh"] = refresh_token_flag
    jwt_token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    return jwt_token


def decode_token(jwt_token: str) -> str:
    token_data = None
    try:
        token_data = jwt.decode(
            jwt=jwt_token,
            key=Config.JWT_SECRET,
            algorithms=Config.JWT_ALGORITHM,
        )
    except PyJWTError as e:
        print(f"Encountered the following error while decoding token: {str(e)}")
    return token_data
