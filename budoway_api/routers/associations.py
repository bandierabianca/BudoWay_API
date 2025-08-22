from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Associations, AssociationsCreate, AssociationsRead, AssociationsUpdate, Users
from ..auth_utils import get_current_user

router = APIRouter(prefix="/associations", tags=["associations"])


# 🔒 Solo utenti loggati possono creare
@router.post("/", response_model=AssociationsRead)
def create_associations(
    payload: AssociationsCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    data = payload.model_dump()
    data["created_by_user"] = current_user.id
    data["last_modified_by_user"] = current_user.id
    data["created_at"] = datetime.now(timezone.utc)
    data["last_modified_at"] = datetime.now(timezone.utc)

    obj = Associations(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# 🌍 pubblico
@router.get("/", response_model=list[AssociationsRead])
def list_associations(session: Session = Depends(get_session)):
    return session.exec(select(Associations)).all()


# 🌍 pubblico
@router.get("/{item_id}", response_model=AssociationsRead)
def get_associations(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Associations, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


# 🔒 Solo utenti loggati possono aggiornare
@router.put("/{item_id}", response_model=AssociationsRead)
def update_associations(
    item_id: int,
    payload: AssociationsUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    obj = session.get(Associations, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)

    obj.last_modified_by_user = current_user.id
    obj.last_modified_at = datetime.now(timezone.utc)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# 🔒 Solo utenti loggati possono eliminare
@router.delete("/{item_id}")
def delete_associations(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    obj = session.get(Associations, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}
