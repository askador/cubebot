from sqlalchemy import BigInteger, CheckConstraint, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from bot.db.base import Base

class Player(Base):
    __tablename__ = 'players'
    __table_args__ = (
        CheckConstraint("money >= 0", name='check_money_positive'), 
        CheckConstraint("won >= 0", name='check_won_positive'), 
        CheckConstraint("loss >= 0", name='check_loss_positive'), 
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(65), nullable=False)
    money = Column(BigInteger, server_default='1000')
    plays_amount = Column(Integer, server_default='0')
    won = Column(BigInteger, server_default='0')
    loss = Column(BigInteger, server_default='0')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"Player(id='{self.id}', fullname='{self.fullname}', money='{self.money}')" 