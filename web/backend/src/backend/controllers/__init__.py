from fastapi import APIRouter


class Controller:
    router: APIRouter
    public_routes: list = []
