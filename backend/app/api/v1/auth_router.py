from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse,UserLogin,TokenResponse
from app.services.auth_service import AuthService, UserAlreadyExistsError,InvalidCredentialsError
from app.models.user import User
from backend.app.api.v1.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.register(user)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=200,
)
def login(
    login_data:UserLogin,
    db:Session = Depends(get_db)
):
    service = AuthService(db)
    try:
        return service.login(login_data)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401,
                    detail="Invalid credentials",)
   
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
