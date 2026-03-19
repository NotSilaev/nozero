from src.database import execute, fetch

from src.utils.common import get_current_datetime

from datetime import datetime, timedelta


class TokensTable:
    @staticmethod
    async def create(user_id: int, refresh_token: str) -> None:
        created_at: datetime = get_current_datetime()

        stmt = """
            INSERT INTO tokens
            (user_id, refresh_token, created_at)
            VALUES ($1, $2, $3)
        """

        params = (user_id, refresh_token, created_at)

        await execute(stmt, params)


    @staticmethod
    async def get(refresh_token: str) -> dict | None:
        query = """
            SELECT id, user_id, refresh_token, created_at
            FROM tokens
            WHERE refresh_token = $1
        """

        params = (refresh_token, )

        response: list = await fetch(query, params, fetch_type="one", as_dict=True)

        try:
            refresh_token: dict = response[0]
        except IndexError:
            refresh_token = None

        return refresh_token
