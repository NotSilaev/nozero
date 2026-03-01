from src.config import settings

import asyncpg
from typing import Any


async def get_database_connection() -> asyncpg.connection.Connection:
    connection = await asyncpg.connect(
        host=settings.DB_HOST, 
        port=settings.DB_PORT,
        database=settings.DB_NAME, 
        user=settings.DB_USER,
        password=settings.DB_PASSWORD, 
    )
    return connection


async def execute(stmt: str, params: tuple, returning: bool = False) -> None | Any:
    """
    Executes an SQL statement query.
    
    :param stmt: SQL statement query.
    :param returning: set to `True` if the sql query contains the `RETURNING` statement.
    """

    connection = await get_database_connection()
    try:
        if returning:
            created_row: tuple = await connection.fetchrow(stmt, *params)
            return created_row
        else:
            await connection.execute(stmt, *params)
    finally:
        await connection.close()


async def fetch(query: str, params: tuple = None, fetch_type: str = "one", as_dict: bool = False) -> list:
    """
    Executes an SQL fetch query.
    
    :param query: SQL fetch query.
    :param fetch_type: if `one`, the fetchone() function will be executed, if `all` - the fetchall().
    :param as_dict: if `True`, returns the response in the dictionary view.
    """

    if not params:
        params = tuple()

    connection = await get_database_connection()
    try:
        match fetch_type:
            case "one": response = await connection.fetchrow(query, *params)
            case "all": response = await connection.fetch(query, *params)
            case _:
                raise ValueError("Invalid fetch_type")
    finally:
        await connection.close()

    if not response:
        response = list()

    if as_dict and response:
        columns = response[0].keys()
        match fetch_type:
            case "one":
                response = [dict(zip(columns, response))]
            case "all":
                response = [dict(zip(columns, row)) for row in response]

    return response
