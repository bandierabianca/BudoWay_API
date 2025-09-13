from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import AuthUser, Users
from ..schemas import UserRegister, Token
from ..auth_utils import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)

from jose import JWTError, jwt
from ..auth_utils import SECRET_KEY, ALGORITHM, oauth2_scheme
from ..models import RevokedToken

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(payload: UserRegister, session: Session = Depends(get_session)):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Trova o crea utente in Users
    user = session.exec(select(Users).where(Users.mail == payload.email)).first()
    if not user:
        user = Users(mail=payload.email)
        session.add(user)
        session.commit()
        session.refresh(user)

    # Verifica se esiste già
    existing_auth = session.exec(select(AuthUser).where(AuthUser.user_id == user.id)).first()
    if existing_auth:
        raise HTTPException(status_code=400, detail="User already registered for authentication")

    # Crea record auth
    hashed_pw = hash_password(payload.password)
    auth_record = AuthUser(user_id=user.id, hashed_password=hashed_pw)
    session.add(auth_record)
    session.commit()
    session.refresh(auth_record)

    # Genera token
    access_token = create_access_token({"sub": str(auth_record.user_id)})
    refresh_token = create_refresh_token({"sub": str(auth_record.user_id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login(payload: UserRegister, session: Session = Depends(get_session)):
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Trova utente
    user = session.exec(select(Users).where(Users.mail == payload.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Trova record auth
    auth_record = session.exec(select(AuthUser).where(AuthUser.user_id == user.id)).first()
    if not auth_record or not auth_record.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(payload.password, auth_record.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Genera token
    access_token = create_access_token({"sub": str(auth_record.user_id)})
    refresh_token = create_refresh_token({"sub": str(auth_record.user_id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Genera nuovo access token
    new_access_token = create_access_token({"sub": str(user_id)})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=400, detail="Token does not contain jti")

        # Inserisci in blacklist
        revoked = RevokedToken(jti=jti)
        session.add(revoked)
        session.commit()

        return {"detail": "Successfully logged out"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")