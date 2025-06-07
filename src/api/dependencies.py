from typing import Optional
from starlette.requests import Request
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.auth_utils import decode_token, is_valid_access_token


class JWTAccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth_credentials = await super().__call__(request)
        if (
            not auth_credentials
            or auth_credentials.scheme.lower() != "bearer"
            or not is_valid_access_token(self.extract_payload_from_token(auth_credentials.credentials))
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authentication credentials",
            )
        return auth_credentials

    def extract_payload_from_token(self, token: str) -> Optional[dict]:
        return decode_token(token)
