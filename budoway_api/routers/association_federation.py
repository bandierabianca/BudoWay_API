from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import AssociationFederation, AssociationFederationCreate, AssociationFederationRead, AssociationFederationUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/association_federation", tags=["association_federation"])

@router.post("/", response_model=AssociationFederationRead, dependencies=[Depends(get_current_auth_user)])
def create_association_federation(payload: AssociationFederationCreate, session: Session = Depends(get_session)):
    obj = AssociationFederation(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[AssociationFederationRead])
def list_association_federation(session: Session = Depends(get_session)):
    return session.exec(select(AssociationFederation)).all()

@router.get("/{item_id}", response_model=AssociationFederationRead)
def get_association_federation(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationFederation, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=AssociationFederationRead, dependencies=[Depends(get_current_auth_user)])
def update_association_federation(item_id: int, payload: AssociationFederationUpdate, session: Session = Depends(get_session)):
    obj = session.get(AssociationFederation, item_id)
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
def delete_association_federation(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationFederation, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
