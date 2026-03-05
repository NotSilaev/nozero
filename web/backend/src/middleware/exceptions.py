from src.logs import Logs

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from typing import Callable, Awaitable
import traceback


async def exceptions_handling_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        log_text = f"{e}\n\n{traceback.format_exc()}"
        Logs.add_log(
            level="ERROR",
            text=log_text
        )

        return JSONResponse(
            status_code=500,
            content={
                "errors": [{
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Something went wrong"
                }]
            }
        )
