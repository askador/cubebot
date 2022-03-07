from sqlalchemy import Column, BigInteger, DateTime, func
from sqlalchemy.orm import relationship

from bot.db.base import Base

class Chat(Base):
    __tablename__ = 'chats'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
       return f"Chat(id='{self.id}')"
