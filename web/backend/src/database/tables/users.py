from src.database import execute, fetch
from src.database.utils import make_query_conditions

from src.utils.common import get_current_datetime

from datetime import datetime


class UsersTable:
    @staticmethod
    async def create(email: str) -> int:
        created_at: datetime = get_current_datetime()

        stmt = """
            INSERT INTO users 
            (email, created_at) 
            VALUES ($1, $2) 
            RETURNING id
        """

        params = (email, created_at)

        user_id: int = await execute(stmt, params, returning=True)
        return user_id


    @staticmethod
    async def get(user_id: int = None, email: str = None) -> dict | None:
        if (not user_id) and (not email):
            raise AttributeError("At least one column must be passed")

        conditions_data: tuple = make_query_conditions(id=user_id, email=email)
        conditions_string, conditions_params = conditions_data

        query = f"""
            SELECT id, email 
            FROM users
            {conditions_string}
        """

        response: list = await fetch(query, conditions_params, fetch_type="one", as_dict=True)

        try:
            user: dict = response[0]
        except IndexError:
            user = None

        return user
