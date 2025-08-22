import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlmodel import Session, select

from budoway_api.database import get_session
from budoway_api.models import Users

# Il tokenUrl è l'endpoint che emette i token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = (
    os.getenv("SECRET_KEY")
    or (lambda: (_ for _ in ()).throw(ValueError("SECRET_KEY non definita")))()
)

REFRESH_SECRET_KEY = (
    os.getenv("REFRESH_SECRET_KEY")
    or (lambda: (_ for _ in ()).throw(ValueError("REFRESH_SECRET_KEY non definita")))()
)
ALGORITHM = (
    os.getenv("ALGORITHM")
    or (lambda: (_ for _ in ()).throw(ValueError("ALGORITHM non definita")))()
)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    or (
        lambda: (_ for _ in ()).throw(
            ValueError("ACCESS_TOKEN_EXPIRE_MINUTES non definita")
        )
    )()
)
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    or (
        lambda: (_ for _ in ()).throw(
            ValueError("REFRESH_TOKEN_EXPIRE_DAYS non definita")
        )
    )()
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def decode_refresh_token(token: str):
    return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user = session.exec(select(Users).where(Users.id == int(user_id))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
