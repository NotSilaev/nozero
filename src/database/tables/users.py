import sys
sys.path.append("../../") # src/

from database import execute, fetch
from database.utils import makeQueryConditions
from utils.common import getCurrentDateTime

import uuid
from datetime import datetime


def createUser(telegram_id: int) -> str:
    user_id = str(uuid.uuid4())
    created_at: datetime = getCurrentDateTime()

    stmt = """
        INSERT INTO users
        (id, telegram_id, created_at)
        VALUES (%s, %s, %s)
    """
    params = (user_id, telegram_id, created_at)

    execute(stmt, params)

    return user_id


def getUser(user_id: str = None, telegram_id: int = None) -> dict | None:
    if (not user_id) and (not telegram_id):
        raise AttributeError("At least one argument must be passed")

    if user_id:
        user_id = f"'{user_id}'::uuid"

    conditions_data: tuple = makeQueryConditions(id=user_id, telegram_id=telegram_id)
    conditions_string = conditions_data[0]
    conditions_params = conditions_data[1]

    query = f"""
        SELECT id, telegram_id, created_at
        FROM users
        {conditions_string}
    """

    response: list = fetch(query, conditions_params, fetch_type="one", as_dict=True)

    try:
        user: dict = response[0]
    except IndexError:
        user = None

    return user
