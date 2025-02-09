from sqlalchemy import Column, Integer, String

from database import Base


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    date = Column(String(), nullable=False)
    number_of_participants = Column(Integer(), nullable=False, default=0)
    participant_ids = Column(String(), nullable=False, default="")
    tags = Column(String(), nullable=False)
