from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv


load_dotenv()
url = os.getenv("DATABASE_URL")
if url is None:
    raise ValueError("DATABASE_URL is not set in environment variables")


engine = create_engine(url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
