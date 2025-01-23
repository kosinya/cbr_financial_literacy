from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(String())
    content = Column(String(), nullable=False)
    image_url = Column(String())
    test_url = Column(String())
    is_event = Column(Boolean(), default=False)
    tags = Column(String(), nullable=False)
