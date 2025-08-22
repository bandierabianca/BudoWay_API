from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import AuthUser, Users
from ..schemas import UserRegister, Token
from ..auth_utils import create_access_token, hash_password, verify_password

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

    # Verifica se esiste già un record auth_users
    existing_auth = session.exec(select(AuthUser).where(AuthUser.user_id == user.id)).first()
    if existing_auth:
        raise HTTPException(status_code=400, detail="User already registered for authentication")

    # Crea record auth con password hashata
    hashed_pw = hash_password(payload.password)
    auth_record = AuthUser(user_id=user.id, hashed_password=hashed_pw)
    session.add(auth_record)
    session.commit()
    session.refresh(auth_record)

    # Token
    token = create_access_token({"sub": str(auth_record.user_id)})
    return {"access_token": token, "token_type": "bearer"}

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

    # Token
    token = create_access_token({"sub": str(auth_record.user_id)})
    return {"access_token": token, "token_type": "bearer"}
