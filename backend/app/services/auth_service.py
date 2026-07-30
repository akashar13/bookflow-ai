from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate, UserLogin,TokenResponse
from app.core.jwt import create_access_token

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass


class AuthService:  
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        

    def register(self,  user_data: UserCreate):
        
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsError()
        hashed_password = hash_password(user_data.password)
        user = User(
        name=user_data.name,
        email=user_data.email,
        mobile=user_data.mobile,
        password_hash=hashed_password,
        )
        try:
            self.user_repository.create(user)
            self.db.commit()
            self.db.refresh(user)

            # print(f"Name: {name}")
            # print(f"Email: {email}")
            # print(f"Hashed Password: {hashed_password}")

            return user
        except Exception as e:
            self.db.rollback()
            raise
        
    def login(self, login_data: UserLogin):
        user = self.user_repository.get_by_email(login_data.email)

        if not user:
            raise InvalidCredentialsError()

        if not verify_password(
            login_data.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError()

        token = create_access_token(
            {
                "sub": user.email
            }
        )

        return TokenResponse(
            access_token=token
            )