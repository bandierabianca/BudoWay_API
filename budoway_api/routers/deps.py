from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..security import decode_token
from ..database import get_session
from sqlmodel import Session
from ..models import AuthUser

security = HTTPBearer()

def get_current_auth_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload["sub"])
    user = session.get(AuthUser, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token or user not found")
    return user
