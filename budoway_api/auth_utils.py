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

import uuid
from budoway_api.models import Users, RevokedToken

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
    jti = str(uuid.uuid4())   # 👈 genera identificativo univoco del token
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "jti": jti})
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


from jwt import ExpiredSignatureError


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> Users:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 👇 controlla se il token è stato revocato
        if jti and session.exec(select(RevokedToken).where(RevokedToken.jti == jti)).first():
            raise HTTPException(
                status_code=401,
                detail="Token revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or malformed token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.exec(select(Users).where(Users.id == int(user_id))).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
