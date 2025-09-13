from typing import Optional, List
import datetime
from sqlmodel import SQLModel, Field, Relationship

class Events(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location: Optional[str] = Field(default=None)
    date_event: Optional[datetime.datetime] = Field(default=None)
    description: Optional[str] = Field(default=None)
    validated_by_admin: Optional[bool] = Field(default=None)
    validated_by_admin_id: Optional[int] = Field(default=None, foreign_key="users.id")
    validated_by_community: Optional[bool] = Field(default=None)
    validated_by_AI: Optional[bool] = Field(default=None)
    created_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime.datetime] = Field(default=None)
    last_modified_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    last_modified_at: Optional[datetime.datetime] = Field(default=None)

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None)
    mail: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    birthday: Optional[datetime.date] = Field(default=None)
    sex: Optional[str] = Field(default=None)
    primary_sport: Optional[int] = Field(default=None, foreign_key="sports.id")
    validated: Optional[bool] = Field(default=None)
    created_at: Optional[datetime.datetime] = Field(default=None)
    last_modified_at: Optional[datetime.datetime] = Field(default=None)

class UserSports(SQLModel, table=True):
    id_user: Optional[int] = Field(default=None, primary_key=True, foreign_key="users.id")
    id_sport: Optional[int] = Field(default=None, primary_key=True, foreign_key="sports.id")

class Sports(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)

class SportVocabulary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_sport: Optional[int] = Field(default=None, foreign_key="sports.id")
    language_id: Optional[int] = Field(default=None, foreign_key="languages.id")

class Languages(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    language: Optional[str] = Field(default=None)
    language_code: Optional[str] = Field(default=None)

class Trainers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    mail: Optional[str] = Field(default=None)
    telephone: Optional[str] = Field(default=None)
    level: Optional[str] = Field(default=None)
    validated_by_admin: Optional[bool] = Field(default=None)
    validated_by_admin_id: Optional[int] = Field(default=None, foreign_key="users.id")
    validated_by_community: Optional[bool] = Field(default=None)
    validated_by_AI: Optional[bool] = Field(default=None)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime.datetime] = Field(default=None)
    last_modified_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    last_modified_at: Optional[datetime.datetime] = Field(default=None)

class Associations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    mail: Optional[str] = Field(default=None)
    telephone: Optional[str] = Field(default=None)
    validated_by_admin: Optional[bool] = Field(default=None)
    validated_by_admin_id: Optional[int] = Field(default=None, foreign_key="users.id")
    validated_by_community: Optional[bool] = Field(default=None)
    validated_by_AI: Optional[bool] = Field(default=None)
    created_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime.datetime] = Field(default=None)
    last_modified_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    last_modified_at: Optional[datetime.datetime] = Field(default=None)

class AssociationsSports(SQLModel, table=True):
    id_association: Optional[int] = Field(default=None, primary_key=True, foreign_key="associations.id")
    id_sport: Optional[int] = Field(default=None, primary_key=True, foreign_key="sports.id")
    schedule: Optional[str] = Field(default=None)

class AssociationUser(SQLModel, table=True):
    id_association: Optional[int] = Field(default=None, primary_key=True, foreign_key="associations.id")
    id_user: Optional[int] = Field(default=None, primary_key=True, foreign_key="users.id")
    role: Optional[str] = Field(default=None)

class AssociationTrainer(SQLModel, table=True):
    id_association: Optional[int] = Field(default=None, primary_key=True, foreign_key="associations.id")
    id_sport: Optional[int] = Field(default=None, primary_key=True, foreign_key="sports.id")
    schedule: Optional[str] = Field(default=None)
    validated_by_admin: Optional[bool] = Field(default=None)
    validated_by_admin_id: Optional[int] = Field(default=None, foreign_key="users.id")
    validated_by_community: Optional[bool] = Field(default=None)
    validated_by_AI: Optional[bool] = Field(default=None)
    created_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime.datetime] = Field(default=None)
    last_modified_by_user: Optional[int] = Field(default=None, foreign_key="users.id")
    last_modified_at: Optional[datetime.datetime] = Field(default=None)

class Federations(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    abbreviation_name: Optional[str] = Field(default=None)
    long_name: Optional[str] = Field(default=None)

class AssociationFederation(SQLModel, table=True):
    id_association: Optional[int] = Field(default=None, primary_key=True, foreign_key="associations.id")
    id_federation: Optional[int] = Field(default=None, primary_key=True, foreign_key="federations.id")

class FederationSport(SQLModel, table=True):
    id_sport: Optional[int] = Field(default=None, primary_key=True, foreign_key="sports.id")
    id_federation: Optional[int] = Field(default=None, primary_key=True, foreign_key="federations.id")

class AuthUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    hashed_password: Optional[str] = Field(default=None)

class EventsCreate(SQLModel):
    id: Optional[int] = None
    location: Optional[str] = None
    date_event: Optional[datetime.datetime] = None
    description: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class EventsRead(SQLModel):
    id: Optional[int] = None
    location: Optional[str] = None
    date_event: Optional[datetime.datetime] = None
    description: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class EventsUpdate(SQLModel):
    id: Optional[int] = None
    location: Optional[str] = None
    date_event: Optional[datetime.datetime] = None
    description: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class UsersCreate(SQLModel):
    id: Optional[int] = None
    username: Optional[str] = None
    mail: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    sex: Optional[str] = None
    primary_sport: Optional[int] = None
    validated: Optional[bool] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_at: Optional[datetime.datetime] = None

class UsersRead(SQLModel):
    id: Optional[int] = None
    username: Optional[str] = None
    # mail hidden for privacy by default
    name: Optional[str] = None
    surname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    sex: Optional[str] = None
    primary_sport: Optional[int] = None
    validated: Optional[bool] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_at: Optional[datetime.datetime] = None

class UsersUpdate(SQLModel):
    id: Optional[int] = None
    username: Optional[str] = None
    mail: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    sex: Optional[str] = None
    primary_sport: Optional[int] = None
    validated: Optional[bool] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_at: Optional[datetime.datetime] = None

class UserSportsCreate(SQLModel):
    pass

class UserSportsRead(SQLModel):
    id_user: int
    id_sport: int

class UserSportsUpdate(SQLModel):
    id_user: Optional[int] = None
    id_sport: Optional[int] = None

class SportsCreate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None

class SportsRead(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None

class SportsUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None

class SportVocabularyCreate(SQLModel):
    id: Optional[int] = None
    id_sport: Optional[int] = None
    language_id: Optional[int] = None

class SportVocabularyRead(SQLModel):
    id: Optional[int] = None
    id_sport: Optional[int] = None
    language_id: Optional[int] = None

class SportVocabularyUpdate(SQLModel):
    id: Optional[int] = None
    id_sport: Optional[int] = None
    language_id: Optional[int] = None

class LanguagesCreate(SQLModel):
    id: Optional[int] = None
    language: Optional[str] = None
    language_code: Optional[str] = None

class LanguagesRead(SQLModel):
    id: Optional[int] = None
    language: Optional[str] = None
    language_code: Optional[str] = None

class LanguagesUpdate(SQLModel):
    id: Optional[int] = None
    language: Optional[str] = None
    language_code: Optional[str] = None

class TrainersCreate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    level: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    user_id: Optional[int] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class TrainersRead(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    level: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    user_id: Optional[int] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class TrainersUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    level: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    user_id: Optional[int] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationsCreate(SQLModel):
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationsRead(SQLModel):
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationsUpdate(SQLModel):
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    mail: Optional[str] = None
    telephone: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationsSportsCreate(SQLModel):
    schedule: Optional[str] = None

class AssociationsSportsRead(SQLModel):
    id_association: int
    id_sport: int
    schedule: Optional[str] = None

class AssociationsSportsUpdate(SQLModel):
    id_association: Optional[int] = None
    id_sport: Optional[int] = None
    schedule: Optional[str] = None

class AssociationUserCreate(SQLModel):
    role: Optional[str] = None

class AssociationUserRead(SQLModel):
    id_association: int
    id_user: int
    role: Optional[str] = None

class AssociationUserUpdate(SQLModel):
    id_association: Optional[int] = None
    id_user: Optional[int] = None
    role: Optional[str] = None

class AssociationTrainerCreate(SQLModel):
    schedule: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationTrainerRead(SQLModel):
    id_association: int
    id_sport: int
    schedule: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class AssociationTrainerUpdate(SQLModel):
    id_association: Optional[int] = None
    id_sport: Optional[int] = None
    schedule: Optional[str] = None
    validated_by_admin: Optional[bool] = None
    validated_by_admin_id: Optional[int] = None
    validated_by_community: Optional[bool] = None
    validated_by_AI: Optional[bool] = None
    created_by_user: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    last_modified_by_user: Optional[int] = None
    last_modified_at: Optional[datetime.datetime] = None

class FederationsCreate(SQLModel):
    id: Optional[int] = None
    abbreviation_name: Optional[str] = None
    long_name: Optional[str] = None

class FederationsRead(SQLModel):
    id: Optional[int] = None
    abbreviation_name: Optional[str] = None
    long_name: Optional[str] = None

class FederationsUpdate(SQLModel):
    id: Optional[int] = None
    abbreviation_name: Optional[str] = None
    long_name: Optional[str] = None

class AssociationFederationCreate(SQLModel):
    pass

class AssociationFederationRead(SQLModel):
    id_association: int
    id_federation: int

class AssociationFederationUpdate(SQLModel):
    id_association: Optional[int] = None
    id_federation: Optional[int] = None

class FederationSportCreate(SQLModel):
    pass

class FederationSportRead(SQLModel):
    id_sport: int
    id_federation: int

class FederationSportUpdate(SQLModel):
    id_sport: Optional[int] = None
    id_federation: Optional[int] = None

class UserRegister(SQLModel):
    user_id: Optional[int] = None
    email: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'


class RevokedToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str  # identificativo univoco del token
    revoked_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
