import json
from json import JSONDecodeError
from typing import Optional
from starlette.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, PyJWTError

# import traceback

from utils.auth_utils import decode_token
from database.redis import blacklist_token, is_blacklisted


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth_credentials = await super().__call__(request)
        if not auth_credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials or invalid scheme in header.",
            )
        token_payload = {}
        try:
            token_payload = decode_token(auth_credentials.credentials)
        except ExpiredSignatureError:
            # traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The provided token has expired.",
            )
        except PyJWTError:
            # traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials provided.",
            )
        self.verify_token_payload(token_payload)
        if await is_blacklisted(token_payload["jti"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This token is invalid or has been revoked.",
            )
        token_payload["sub"] = self.deserialize_user_data(token_payload["sub"])
        return token_payload

    def verify_token_payload(self, token_payload: dict) -> None:
        raise NotImplementedError("No implementation found. Please override this method in child class.")

    def deserialize_user_data(self, user_data_str: str) -> dict:
        user_data = {}
        try:
            user_data = json.loads(user_data_str)
            if not isinstance(user_data, dict):
                raise ValueError("Payload's subject doesn't have a valid dictionary.")
        except (JSONDecodeError, TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid subject format in token's payload.",
            )
        return user_data


class JWTAccessTokenBearer(TokenBearer):
    def verify_token_payload(self, token_payload: dict) -> None:
        if token_payload["is_refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token found. Please provide a valid access token.",
            )


class JWTRefreshTokenBearer(TokenBearer):
    def verify_token_payload(self, token_payload: dict) -> None:
        if not token_payload["is_refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token found. Please provide a valid refresh token.",
            )
