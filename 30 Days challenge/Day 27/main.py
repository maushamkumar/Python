from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

engine = create_engine('sqlite:///example.db')  # You can use PostgreSQL or MySQL too
Base.metadata.create_all(engine)  # Creates tables based on your class definitions


Session = sessionmaker(bind=engine)
session = Session()


new_user = User(name="Sam", email="sam@example.com")
session.add(new_user)
session.commit()

user = session.query(User).filter_by(name="Sam").first()
print(user.email)
