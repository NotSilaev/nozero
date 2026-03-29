from src.core.config import settings

from src.middleware.exceptions import exceptions_handling_middleware
from src.middleware.auth import auth_middleware
from src.middleware.rate import rate_limiting_middleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.base import BaseHTTPMiddleware


class MiddlewareManager:
    middleware = [
        {
            "middleware_class": BaseHTTPMiddleware,
            "dispatch": auth_middleware,
        },
        {
            "middleware_class": BaseHTTPMiddleware,
            "dispatch": rate_limiting_middleware,
        },
        {
            "middleware_class": BaseHTTPMiddleware,
            "dispatch": exceptions_handling_middleware,
        },
        {
            "middleware_class": CORSMiddleware,
            "allow_origins": settings.CORS_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    ]

    def connect(self, app: FastAPI) -> None:
        for mw_kwargs in self.middleware:
            app.add_middleware(**mw_kwargs)
