from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import UserSports, UserSportsCreate, UserSportsRead, UserSportsUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/user_sports", tags=["user_sports"])

@router.post("/", response_model=UserSportsRead, dependencies=[Depends(get_current_auth_user)])
def create_user_sports(payload: UserSportsCreate, session: Session = Depends(get_session)):
    obj = UserSports(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[UserSportsRead])
def list_user_sports(session: Session = Depends(get_session)):
    return session.exec(select(UserSports)).all()

@router.get("/{item_id}", response_model=UserSportsRead)
def get_user_sports(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(UserSports, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=UserSportsRead, dependencies=[Depends(get_current_auth_user)])
def update_user_sports(item_id: int, payload: UserSportsUpdate, session: Session = Depends(get_session)):
    obj = session.get(UserSports, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{item_id}", dependencies=[Depends(get_current_auth_user)])
def delete_user_sports(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(UserSports, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
