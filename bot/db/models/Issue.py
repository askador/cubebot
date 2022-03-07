from sqlalchemy import Boolean, Column, BigInteger, DateTime, Text, func
from sqlalchemy.orm import relationship

from bot.db.base import Base

class Issue(Base):
    __tablename__ = 'issues'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    link = Column(Text, nullable=False)
    is_open = Column(Boolean, nullable=False, server_default='1')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
       return f"Issue(id='{self.id}', link='{self.link}', is_open='{self.is_open}')"
