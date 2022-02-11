from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from bot.db.base import Base

class Game(Base):
    __tablename__ = 'games'

    chat_id = Column(BigInteger, ForeignKey("chats.id", ondelete="cascade", onupdate="cascade"), primary_key=True)
    is_rolling = Column(Boolean, nullable=False, server_default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    def __repr__(self):
       return f"Game(chat_id={self.chat_id}')" 