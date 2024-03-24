from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base

# TODO Externalize your database URI to an environment variable or config file
DATABASE_URI = 'sqlite:///planner.db'  

engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
