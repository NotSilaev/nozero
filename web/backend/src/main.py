from src.middleware.exceptions import exceptions_handling_middleware

from fastapi import FastAPI

from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()


# Middleware
app.add_middleware(
    BaseHTTPMiddleware, 
    dispatch=exceptions_handling_middleware
)
