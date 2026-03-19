from src.database import execute, fetch

from src.utils.common import get_current_datetime

from datetime import datetime


class CodesTable:
    @staticmethod
    async def create(email: str, code: str) -> None:
        created_at: datetime = get_current_datetime()

        stmt = """
            INSERT INTO codes
            (email, code, created_at)
            VALUES ($1, $2, $3)
        """

        params = (email, code, created_at)

        await execute(stmt, params)


    @staticmethod
    async def get(email: str, code: str) -> dict | None:
        query = """
            SELECT id, email, code, created_at
            FROM codes
            WHERE email = $1 AND code = $2
        """

        params = (email, code)

        response: list = await fetch(query, params, fetch_type="one", as_dict=True)

        try:
            code: dict = response[0]
        except IndexError:
            code = None

        return code
