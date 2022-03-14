from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from bot.db.base import Base

class ChatLog(Base):
    __tablename__ = 'chats_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("chats.id", ondelete="cascade", onupdate="cascade") ,nullable=False)
    log = Column(String(2), nullable=False)

    def __repr__(self):
       return f"ChatLog(chat_id='{self.chat_id}', log='{self.log}')"
