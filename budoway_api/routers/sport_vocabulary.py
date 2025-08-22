from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import SportVocabulary, SportVocabularyCreate, SportVocabularyRead, SportVocabularyUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/sport_vocabulary", tags=["sport_vocabulary"])

@router.post("/", response_model=SportVocabularyRead, dependencies=[Depends(get_current_auth_user)])
def create_sport_vocabulary(payload: SportVocabularyCreate, session: Session = Depends(get_session)):
    obj = SportVocabulary(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[SportVocabularyRead])
def list_sport_vocabulary(session: Session = Depends(get_session)):
    return session.exec(select(SportVocabulary)).all()

@router.get("/{item_id}", response_model=SportVocabularyRead)
def get_sport_vocabulary(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(SportVocabulary, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=SportVocabularyRead, dependencies=[Depends(get_current_auth_user)])
def update_sport_vocabulary(item_id: int, payload: SportVocabularyUpdate, session: Session = Depends(get_session)):
    obj = session.get(SportVocabulary, item_id)
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
def delete_sport_vocabulary(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(SportVocabulary, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
