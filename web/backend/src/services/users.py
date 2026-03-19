from src.database.tables.users import UsersTable

from src.services.codes import CodesService
from src.services.tokens import TokensService

from src.exceptions.users import LoginError
from src.exceptions.auth import UnauthorizedError


class UsersService:
    @staticmethod
    async def login(email: str, code: str) -> dict:
        is_code_valid: bool = await CodesService.is_code_valid(email, code)
        if not is_code_valid:
            raise LoginError("Invalid code")
        
        user: dict | None = await UsersTable.get(email=email)
        if not user:
            user_id: int = await UsersTable.create(email=email)
            user: dict = {"id": user_id, "email": email}

        tokens: dict = await TokensService.generate_tokens(payload=user)
        refresh_token: str = tokens["refresh_token"]
        await TokensService.save_refresh_token(user_id=user["id"], refresh_token=refresh_token)

        user_data = {"user": user, "tokens": tokens}
        return user_data


    @staticmethod
    async def refresh(refresh_token: str) -> dict:
        if not refresh_token:
            raise UnauthorizedError("Invalid refresh_token")
        
        token_payload: dict = await TokensService.verify_token(token_type="refresh", token=refresh_token)
        token_data: dict = await TokensService.find_refresh_token(refresh_token=refresh_token)

        if (not token_payload) or (not token_data):
            raise UnauthorizedError("Invalid refresh_token")
        
        user_id: int = token_payload["id"]
        user: dict = await UsersTable.get(user_id=user_id)

        tokens: dict = await TokensService.generate_tokens(payload=user)
        refresh_token: str = tokens["refresh_token"]
        await TokensService.save_refresh_token(user_id=user_id, refresh_token=refresh_token)

        user_data = {"user": user, "tokens": tokens}
        return user_data
