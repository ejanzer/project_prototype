import bcrypt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///menureader.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

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
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    #chin_name = Column(String(64), nullable=True)
    #location?
    #yelp url?
    #dianping url?

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    text = Column(String(64), nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User", backref=backref("reviews", order_by=id))
    dish = relationship("Dish", backref=backref("reviews", order_by=id))
    rest_dish = relationship("Rest_Dish", backref=backref("reviews", order_by=id))

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    #img_url = Column(String(64), nullable=False)

class Rest_Dish(Base):
    __tablename__ = "rest_dishes"

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    rest_id = Column(Integer, ForeignKey('restaurants.id'))

    dish = relationship("Dish", backref=backref("rest_dishes", order_by=id))
    restaurant = relationship("Restaurant", backref=backref("rest_dishes", order_by=id))

class Dish_Tag(Base):
    __tablename__ = "dish_tags"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id')) 

    tag = relationship("Tag", backref=backref("dish_tags", order_by=id))
    dish = relationship("Dish", backref=backref("dish_tags", order_by=id))
    rest_dish = relationship("Rest_Dish", backref=backref("dish_tags", order_by=id))

# class Images(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True)
#     rest_dish_id = Column(Integer, ForeignKey('rest_dishes.id'))

#     rest_dish = relationship("Rest_Dish", backref=backref("images", order_by=id))

### End class declarations

def find_combinations(text):
    """Find all combinations of sequential characters within a string of characters."""
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
    """Look through a list of possible word combinations to find a valid set, 
    and return Entry objects associated with each word."""
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


def main():
    # Uncomment and run model.py as main to create schema
   Base.metadata.create_all(engine) 

if __name__ == "__main__":
    main()