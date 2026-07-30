from app.core.config import settings
from datetime import timedelta, timezone, datetime
from jose import jwt,JWTError


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class InvalidTokenError(Exception):
    pass

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
)-> str:
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = data.copy()
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    # add exp claim

    # encode JWT

    return encoded_jwt

def verify_access_token(token)-> str:
    try:
        payload = jwt.decode(token,
                            SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise InvalidTokenError
    email = payload.get("sub")

    if email is None:
            raise InvalidTokenError()


    return email