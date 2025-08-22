from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Languages, LanguagesCreate, LanguagesRead, LanguagesUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/languages", tags=["languages"])

@router.post("/", response_model=LanguagesRead, dependencies=[Depends(get_current_auth_user)])
def create_languages(payload: LanguagesCreate, session: Session = Depends(get_session)):
    obj = Languages(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[LanguagesRead])
def list_languages(session: Session = Depends(get_session)):
    return session.exec(select(Languages)).all()

@router.get("/{item_id}", response_model=LanguagesRead)
def get_languages(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Languages, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=LanguagesRead, dependencies=[Depends(get_current_auth_user)])
def update_languages(item_id: int, payload: LanguagesUpdate, session: Session = Depends(get_session)):
    obj = session.get(Languages, item_id)
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
def delete_languages(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Languages, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
