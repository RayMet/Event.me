"""SQLAlchemy model for table tags"""
from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Tag(Base):
    """SQLAlchemy model for table tags"""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False, unique=True)

    event_tag = relationship("EventTag")
