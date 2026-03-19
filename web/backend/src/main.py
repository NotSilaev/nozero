from src.core.config import settings

from src.managers.controllers import ControllerMananger
from src.managers.middleware import MiddlewareManager

from fastapi import FastAPI


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION
)


controller_manager = ControllerMananger()
controller_manager.connect(app)


middleware_manager = MiddlewareManager()
middleware_manager.connect(app)
