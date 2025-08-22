from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Events, EventsCreate, EventsRead, EventsUpdate, Users
from ..auth_utils import get_current_user


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventsRead)
def create_event(
    event: EventsCreate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    # creiamo un nuovo evento, ignorando created_by_user dal body
    new_event = Events(
        **event.model_dump(exclude={"created_by_user", "last_modified_by_user", "created_at", "last_modified_at"}),
        created_by_user=current_user.id,
        last_modified_by_user=current_user.id,
        created_at=datetime.now(timezone.utc),
        last_modified_at=datetime.now(timezone.utc),
    )

    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event


@router.get("/", response_model=list[EventsRead])
def list_events(session: Session = Depends(get_session)):
    return session.exec(select(Events)).all()


@router.get("/{item_id}", response_model=EventsRead)
def get_events(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Events, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{item_id}", response_model=EventsRead)
def update_events(
    item_id: int,
    event: EventsUpdate,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    obj = session.get(Events, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    #  exclude_unset=True significa: tienimi solo i campi che l’utente ha effettivamente inviato nella request JSON. Se un campo non è stato inviato → non comparirà nel dict.
    data = event.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)

    # Aggiorna i metadati di audit
    obj.last_modified_by_user = current_user.id
    obj.last_modified_at = datetime.now(
        timezone.utc
    )  # 👈 meglio usare utc, così è consistente

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/{item_id}", dependencies=[Depends(get_current_user)])
def delete_events(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Events, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}
