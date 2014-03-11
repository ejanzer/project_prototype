from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class Entry(Base):
    __tablename__ = "cedict"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64))
    traditional = Column(String(64))
    pinyin = Column(String(64))
    definition = Column(String(64))


### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///chindict.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


def main():
   connect()
   Base.metadata.create_all(ENGINE) 

if __name__ == "__main__":
    main()