from src.controllers.users import UsersController

from fastapi import FastAPI


class ControllerMananger:
    controllers = [
        UsersController,
    ]

    controllers_public_routes = [
        public_route 
        for controller in controllers 
        for public_route in controller.public_routes
    ]

    def connect(self, app: FastAPI) -> None:
        for controller in self.controllers:
            app.include_router(controller.router)
