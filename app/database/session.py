from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import Settings

engine = create_engine(url=Settings.database_url,
                       echo=False)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()