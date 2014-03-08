from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    # ratings relationship with User is defined in Rating class


class Movie(Base):
    __tablename__= "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(150), nullable=False)

    # rating relationship with Movie is defined in Rating class

class Rating(Base):
    __tablename__= "ratings"    

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)

    # define relationships of User class with ratings AND Movie class with ratings 
    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))
### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///movies.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
