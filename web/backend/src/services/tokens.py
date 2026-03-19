from src.core.config import settings

from src.database.tables.tokens import TokensTable

from src.utils.common import get_current_datetime

from fastapi import Response

import jwt
from datetime import datetime, timedelta


class TokensService:
    @staticmethod
    async def generate_tokens(payload: dict) -> dict:
        access_token_payload = payload.copy()
        refresh_token_payload = payload.copy()

        now: datetime = get_current_datetime()

        access_token_payload["exp"] = now + timedelta(seconds=settings.JWT_ACCESS_TTL_SECONDS)
        refresh_token_payload["exp"] = now + timedelta(seconds=settings.JWT_REFRESH_TTL_SECONDS)

        access_token: str = jwt.encode(
            payload=access_token_payload,
            key=settings.JWT_ACCESS_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        refresh_token: str = jwt.encode(
            payload=refresh_token_payload,
            key=settings.JWT_REFRESH_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens
    

    @staticmethod
    def set_refresh_token_cookie(response: Response, refresh_token: str) -> Response:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.JWT_REFRESH_TTL_SECONDS,
            httponly=True,
            secure=True
        )
        return response


    @staticmethod
    async def save_refresh_token(user_id: int, refresh_token: str) -> None:
        await TokensTable.create(
            user_id=user_id,
            refresh_token=refresh_token
        )


    @staticmethod
    async def find_refresh_token(refresh_token) -> dict | None:
        token_data: dict | None = await TokensTable.get(refresh_token)
        return token_data


    @staticmethod
    async def verify_token(token_type: str, token: str) -> dict | None:
        token_secrets = {
            "access": settings.JWT_ACCESS_SECRET,
            "refresh": settings.JWT_REFRESH_SECRET
        }

        if token_type.lower() not in token_secrets.keys():
            raise ValueError("Invalid token_type")

        try:
            decoded_payload: dict = jwt.decode(
                jwt=token, 
                key=token_secrets[token_type.lower()],
                algorithms=[settings.JWT_ALGORITHM]
            )
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
