from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    tg_id = Column(Integer(), nullable=False)
    surname = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    patronymic = Column(String())
    age = Column(Integer(), nullable=False)
    region = Column(String(), nullable=False)
    education = Column(String())
    is_admin = Column(Boolean(), default=False, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
