from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import AssociationUser, AssociationUserCreate, AssociationUserRead, AssociationUserUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/association_user", tags=["association_user"])

@router.post("/", response_model=AssociationUserRead, dependencies=[Depends(get_current_auth_user)])
def create_association_user(payload: AssociationUserCreate, session: Session = Depends(get_session)):
    obj = AssociationUser(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[AssociationUserRead])
def list_association_user(session: Session = Depends(get_session)):
    return session.exec(select(AssociationUser)).all()

@router.get("/{item_id}", response_model=AssociationUserRead)
def get_association_user(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationUser, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=AssociationUserRead, dependencies=[Depends(get_current_auth_user)])
def update_association_user(item_id: int, payload: AssociationUserUpdate, session: Session = Depends(get_session)):
    obj = session.get(AssociationUser, item_id)
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
def delete_association_user(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(AssociationUser, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
