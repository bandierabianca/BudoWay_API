from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import FederationSport, FederationSportCreate, FederationSportRead, FederationSportUpdate
from .deps import get_current_auth_user

router = APIRouter(prefix="/federation_sport", tags=["federation_sport"])

@router.post("/", response_model=FederationSportRead, dependencies=[Depends(get_current_auth_user)])
def create_federation_sport(payload: FederationSportCreate, session: Session = Depends(get_session)):
    obj = FederationSport(**payload.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/", response_model=list[FederationSportRead])
def list_federation_sport(session: Session = Depends(get_session)):
    return session.exec(select(FederationSport)).all()

@router.get("/{item_id}", response_model=FederationSportRead)
def get_federation_sport(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(FederationSport, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{item_id}", response_model=FederationSportRead, dependencies=[Depends(get_current_auth_user)])
def update_federation_sport(item_id: int, payload: FederationSportUpdate, session: Session = Depends(get_session)):
    obj = session.get(FederationSport, item_id)
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
def delete_federation_sport(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(FederationSport, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return { "ok": True }
