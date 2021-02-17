from fastapi.routing import APIRouter

from .endpoints import login, users

router = APIRouter()
router.include_router(login.router, prefix="/login", tags=["Login"])
router.include_router(users.router, prefix="/users", tags=["Users"])
