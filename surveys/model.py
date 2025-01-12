from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    date = Column(String(), nullable=False)
    number_of_attempts = Column(Integer())
    filename = Column(String(), nullable=False)
    tags = Column(String())

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'), nullable=False)
    date = Column(String(), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    score = Column(Integer(), nullable=False)