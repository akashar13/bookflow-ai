from fastapi import APIRouter

from app.schemas.user import UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

service = AuthService()


@router.post("/register")
def register(user: UserRegister):
    return service.register(
        user.name,
        user.email,
        user.password
    )