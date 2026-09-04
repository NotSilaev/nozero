from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    code: str | None = None
