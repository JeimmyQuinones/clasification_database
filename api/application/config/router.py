from fastapi import APIRouter

from api.application.controllers import (
    user_controller,
    login_controller,
    database_controller,
)

api_router = APIRouter()
api_router.include_router(user_controller.router, prefix="/users", tags=["users"])
api_router.include_router(login_controller.router, prefix="/login", tags=["login"])
api_router.include_router(
    database_controller.router, prefix="/database", tags=["database"]
)
