from sqlalchemy import BigInteger, CheckConstraint, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from bot.db.base import Base

class Bet(Base):
    __tablename__ = 'bets'
    __table_args__ = (
        CheckConstraint("amount > 0", name='check_amount_positive'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id', ondelete="cascade", onupdate="cascade"), nullable=False)
    chat_id = Column(BigInteger, ForeignKey('games.chat_id', ondelete="cascade", onupdate="cascade"), nullable=False)
    amount = Column(BigInteger, nullable=False)
    numbers = Column(String(4), nullable=False)

    def __repr__(self):
       return f"Bet(user_id='{self.player_id}', chat_id='{self.chat_id}', amount='{self.amount}', numbers='{self.numbers}')"

