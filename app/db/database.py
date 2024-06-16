from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

#DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/TFM"
DATABASE_URL = settings.DATABASE_URL
#interactua con la bbdd
engine = create_engine(DATABASE_URL)

#interactua con la bbdd pero lo que hace es saber como estan los datos actualmente.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

#Devuelve la sesión de la bbdd y cierra la conexión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()