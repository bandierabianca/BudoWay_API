from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import AssociationsSports, AssociationsSportsCreate, AssociationsSportsRead, AssociationsSportsUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/associations_sports", tags=["associations_sports"])

@router.post("/", response_model=AssociationsSportsRead, dependencies=[Depends(get_current_auth_user)])
def create_associations_sports(payload: AssociationsSportsCreate, session: Session = Depends(get_session)):
    obj = AssociationsSports(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[AssociationsSportsRead])
def list_associations_sports(session: Session = Depends(get_session)):
    return session.exec(select(AssociationsSports)).all()

@router.get("/{item_id}", response_model=AssociationsSportsRead)
def get_associations_sports(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationsSports, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=AssociationsSportsRead, dependencies=[Depends(get_current_auth_user)])
def update_associations_sports(item_id: int, payload: AssociationsSportsUpdate, session: Session = Depends(get_session)):
    obj = session.get(AssociationsSports, item_id)
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
def delete_associations_sports(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationsSports, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
