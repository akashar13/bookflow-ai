from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse,UserLogin,TokenResponse
from app.core.jwt import verify_access_token,InvalidTokenError
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService, UserAlreadyExistsError,InvalidCredentialsError
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    email = verify_access_token(token)

    user = UserRepository(db).get_by_email(email)

    if user is None:
        raise InvalidTokenError()

    return user