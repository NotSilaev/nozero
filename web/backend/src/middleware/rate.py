from src.core.rate import RateManager

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from typing import Callable, Awaitable


async def rate_limiting_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    rate_manager = RateManager(request=request)

    if rate_manager.is_request_approved():
        response = await call_next(request)
        rate_manager.process_request()
        return response
    else:
        return JSONResponse(
            status_code=429,
            content={
                "errors": [{
                    "code": "RATE_LIMIT_REACHED",
                    "message": "Too Many Requests"
                }]
            }
        )
