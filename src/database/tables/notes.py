import sys
sys.path.append("../../") # src/

from database import execute, fetch
from utils.common import getCurrentDateTime

import uuid
from datetime import datetime


def createNote(user_id: str, text: str) -> str:
    note_id = str(uuid.uuid4())
    created_at: datetime = getCurrentDateTime()

    stmt = """
        INSERT INTO notes
        (id, user_id, text, created_at)
        VALUES (%s, %s, %s, %s)
    """
    params = (note_id, user_id, text, created_at)

    execute(stmt, params)

    return note_id
