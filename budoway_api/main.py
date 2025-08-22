from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth
from .routers import events
from .routers import users
from .routers import user_sports
from .routers import sports
from .routers import sport_vocabulary
from .routers import languages
from .routers import trainers
from .routers import associations
from .routers import associations_sports
from .routers import association_user
from .routers import association_trainer
from .routers import federations
from .routers import association_federation
from .routers import federation_sport

app = FastAPI(title='BudoWay API - Full features')
models.SQLModel.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(user_sports.router)
app.include_router(sports.router)
app.include_router(sport_vocabulary.router)
app.include_router(languages.router)
app.include_router(trainers.router)
app.include_router(associations.router)
app.include_router(associations_sports.router)
app.include_router(association_user.router)
app.include_router(association_trainer.router)
app.include_router(federations.router)
app.include_router(association_federation.router)
app.include_router(federation_sport.router)

@app.get('/')
def root():
    return {'status':'ok'}
