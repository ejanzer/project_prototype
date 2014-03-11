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

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    simplified = Column(String(64))
    traditional = Column(String(64))
    pinyin = Column(String(64))
    description = Column(String(64))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    password = Column(String(64))

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    #user_id
    #dish_id
    text = Column(String(64))

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    text = Column(String(64))
    url = Column(String(64))

class Tag_Assoc(Base):
    __tablename__ = "tag_assocs"

    id = Column(Integer, primary_key=True)
    #tag_id
    #dish_id 


### End class declarations

def find_combinations(text):
    length = len(text)
    n = length - 1
    num_combos = 2 ** (length - 1)

    bins = []
    for i in range(num_combos):
        num = bin(i).rsplit('b', 1)[1]
        num_str = num.zfill(n)
        bins.append(num_str)

    total_combos = []
    for binary_num in bins:
        combo = []
        for i in range(n):
            if binary_num[i] == '1':
                combo.append(text[i])
                combo.append(',')
            else:
                combo.append(text[i])

        combo.append(text[-1])
        combo = ''.join(combo)
        combo = combo.split(',')
        total_combos.append(combo)
    return total_combos   


def search(combinations):
    session = connect()
    for c in combinations:
        found_def = True
        chars = []
        for char in c:
            entry = session.query(Entry).filter_by(simplified=char).first()
            if entry:
                chars.append(entry)
            else:
                found_def = False
                break
        
        if found_def:
            return chars

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