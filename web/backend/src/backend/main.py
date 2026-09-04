from backend.core.config import settings

from backend.managers.controllers import ControllerMananger
from backend.managers.middleware import MiddlewareManager

from fastapi import FastAPI


app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION
)


controller_manager = ControllerMananger()
controller_manager.connect(app)


middleware_manager = MiddlewareManager()
middleware_manager.connect(app)
