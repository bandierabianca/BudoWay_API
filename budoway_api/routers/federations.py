from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Federations, FederationsCreate, FederationsRead, FederationsUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/federations", tags=["federations"])

@router.post("/", response_model=FederationsRead, dependencies=[Depends(get_current_auth_user)])
def create_federations(payload: FederationsCreate, session: Session = Depends(get_session)):
    obj = Federations(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[FederationsRead])
def list_federations(session: Session = Depends(get_session)):
    return session.exec(select(Federations)).all()

@router.get("/{item_id}", response_model=FederationsRead)
def get_federations(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Federations, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=FederationsRead, dependencies=[Depends(get_current_auth_user)])
def update_federations(item_id: int, payload: FederationsUpdate, session: Session = Depends(get_session)):
    obj = session.get(Federations, item_id)
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
def delete_federations(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Federations, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
