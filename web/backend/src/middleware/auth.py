from src.managers.controllers import ControllerMananger

from src.services.tokens import TokensService

from src.exceptions.auth import UnauthorizedError, AlreadyAuthorizedError

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from typing import Callable, Awaitable



async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_path: str = request.scope["path"]

    controller_manager = ControllerMananger()
    public_routes: list = controller_manager.controllers_public_routes
    if request_path in public_routes:
        return await handle_public_route(request, call_next)
    
    return await handle_protected_route(request, call_next)


async def handle_public_route(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        authorization_header: str = request.headers.get("Authorization")
        if authorization_header:
            access_token: str = authorization_header.split()[1]
            if access_token:
                user_data: dict = await TokensService.verify_token(token_type="access", token=access_token)
                if user_data:
                    raise AlreadyAuthorizedError
                
        return await call_next(request)
    
    except AlreadyAuthorizedError:
        return JSONResponse(
            status_code=403,
            content={
                "errors": [{
                    "code": "FORBIDDEN",
                    "message": "Already authorized"
                }]
            }
        )


async def handle_protected_route(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        authorization_header: str = request.headers.get("Authorization")
        if not authorization_header:
            raise UnauthorizedError("Authorization header doesn't exist")
        
        access_token: str = authorization_header.split()[1]
        if not access_token:
            raise UnauthorizedError("access_token doesn't exist")
        
        user_data: dict = await TokensService.verify_token(token_type="access", token=access_token)
        if not user_data:
            raise UnauthorizedError("Invalid access_token")

        request.state.user = user_data
        return await call_next(request)
    
    except UnauthorizedError:
        return JSONResponse(
            status_code=401,
            content={
                "errors": [{
                    "code": "UNAUTHORIZED",
                    "message": "Unauthorized"
                }]
            }
        )

