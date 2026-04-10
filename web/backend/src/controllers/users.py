from src.core.rate import rate_limiter

from src.controllers import Controller

from src.models.users import LoginRequest

from src.services.codes import CodesService
from src.services.users import UsersService
from src.services.tokens import TokensService

from src.validators.emails import EmailsValidator

from src.exceptions.users import LoginError
from src.exceptions.auth import UnauthorizedError

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


class UsersController(Controller):
    router = APIRouter(
        prefix="/users",
        tags=["users"]
    )
    public_routes = ["/users/login", "/users/refresh", "/docs", "/openapi.json"]


router = UsersController.router


@router.post("/login")
@rate_limiter(max_requests=3, window_seconds=30)
async def login(login_request: LoginRequest, request: Request) -> JSONResponse:
    is_email_valid: bool = EmailsValidator(email=login_request.email).is_email_valid()
    if not is_email_valid:
        return JSONResponse(
            status_code=400,
            content={"errors": [{"code": "BAD_REQUEST", "message": "Invalid email"}]}
        )

    if not login_request.code:
        await CodesService.send_code(login_request.email)
        return JSONResponse(status_code=200, content={"message": "OK"})
    
    try:
        user_data: dict = await UsersService.login(
            email=login_request.email, 
            code=login_request.code
        )
    except LoginError as e:
        message = str(e) if e else "Login error"
        return JSONResponse(
            status_code=400,
            content={"errors": [{"code": "BAD_REQUEST", "message": message}]}
        )

    await CodesService.delete_code(
        email=login_request.email,
        code=login_request.code
    )

    response = JSONResponse(status_code=200, content=user_data)
    response: JSONResponse = TokensService.set_refresh_token_cookie(
        response=response, 
        refresh_token=user_data["tokens"]["refresh_token"]
    )
    return response


@router.get("/refresh")
async def refresh(request: Request) -> JSONResponse:
    refresh_token: str = request.cookies.get("refresh_token")

    try:
        user_data = await UsersService.refresh(refresh_token=refresh_token)
    except UnauthorizedError as e:
        message = str(e) if e else "Unauthorized"
        return JSONResponse(
            status_code=401,
            content={"errors": [{"code": "UNAUTHORIZED", "message": message}]}
        )

    response = JSONResponse(status_code=200, content=user_data)
    response: JSONResponse = TokensService.set_refresh_token_cookie(
        response=response, 
        refresh_token=user_data["tokens"]["refresh_token"]
    )
    return response
