from sqlalchemy import Column, Integer, String

from database import Base


class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    date = Column(String(), nullable=False)
    number_of_attempts = Column(Integer())
    filename = Column(String(), nullable=False)
    tags = Column(String())
