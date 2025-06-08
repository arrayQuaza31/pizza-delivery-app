from typing import Optional
from starlette.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, PyJWTError

# import traceback

from utils.auth_utils import decode_token


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
        return token_payload

    def verify_token_payload(self, token_payload: dict) -> None:
        raise NotImplementedError("No implementation found. Please override this method in child class.")


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
