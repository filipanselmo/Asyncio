from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base


PG_DSN = 'postgresql://admin:admin@127.0.0.1:5432/swapi_db'
db_engine = create_engine(PG_DSN)
Base = declarative_base()





class CharModel(Base):

    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(100), nullable=False)
    eye_color = Column(String(100), nullable=False)
    films = Column(String(1000), nullable=False)
    gender = Column(String(100), nullable=False)
    hair_color = Column(String(100), nullable=False)
    height = Column(String(100), nullable=False)
    homeworld = Column(String(100), nullable=False)
    mass = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    skin_color = Column(String(100), nullable=False)
    species = Column(String(1000), nullable=False)
    starships = Column(String(1000), nullable=False)
    vehicles = Column(String(1000), nullable=False)



Base.metadata.create_all(db_engine)