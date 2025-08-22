from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from budoway_api.auth_utils import get_current_user
from ..database import get_session
from ..models import Users, UsersCreate, UsersRead, UsersUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UsersRead)
def create_users(
    user: UsersCreate,
    session: Session = Depends(get_session),
):

    # creiamo un nuovo utente, ignorando created_by_user dal body
    new_user = Users(
        **user.model_dump(),
        created_at=datetime.now(timezone.utc),
        last_modified_at=datetime.now(timezone.utc),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UsersRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(Users)).all()


@router.get("/{item_id}", response_model=UsersRead)
def get_users(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Users, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put(
    "/{item_id}",
    response_model=UsersRead,
    dependencies=[Depends(get_current_user)],
)
def update_users(
    item_id: int, user: UsersUpdate, session: Session = Depends(get_session)
):
    obj = session.get(Users, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    #  exclude_unset=True significa: tienimi solo i campi che l’utente ha effettivamente inviato nella request JSON. Se un campo non è stato inviato → non comparirà nel dict.
    data = user.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)

        obj.last_modified_at = datetime.now(timezone.utc)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/{item_id}", dependencies=[Depends(get_current_user)])
def delete_users(item_id: int, session: Session = Depends(get_session)):
    obj = session.get(Users, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}
