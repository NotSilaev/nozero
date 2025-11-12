import sys
sys.path.append("../../") # src/

from database import execute, fetch
from database.utils import makeQueryConditions

from utils.common import getCurrentDateTime

from datetime import datetime


def createNote(user_id: str, text: str) -> None:
    created_at: datetime = getCurrentDateTime()
    stmt = """
        INSERT INTO notes
        (user_id, text, created_at)
        VALUES (%s, %s, %s)
    """
    params = (user_id, text, created_at)
    execute(stmt, params)


def getNotes(user_id: str = None) -> list:
    if user_id:
        user_id = f"'{user_id}'::uuid"

    conditions_data: tuple = makeQueryConditions(user_id=user_id)
    conditions_string = conditions_data[0]
    conditions_params = conditions_data[1]

    query = f"""
        SELECT id, user_id, text, created_at
        FROM notes
        {conditions_string}
    """
    notes: list = fetch(query, fetch_type="all", as_dict=True)
    return notes


def getNote(note_id: int) -> dict | None:
    query = """
        SELECT id, user_id, text, created_at
        FROM notes
        WHERE id = %s
    """
    params = (note_id, )

    response: list = fetch(query, params, fetch_type="one", as_dict=True)

    try:
        note: dict = response[0]
    except IndexError:
        note = None

    return note
