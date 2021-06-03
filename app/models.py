from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key=True,
    )
    username = Column(
        String(100),
        nullable=False,
        unique=True,
    )
    password = Column(String())
    wallet = relationship('Wallet', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Wallet(Base):

    __tablename__ = 'wallet'

    id = Column(
        Integer,
        primary_key=True,
    )
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='wallet')
    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship('Currency')
    balance = Column(DECIMAL(12, 2), nullable=False)

    outgoing_transfers = relationship(
        'Transfer', foreign_keys='transfer.c.from_wallet_id'
    )
    incoming_transfers = relationship(
        'Transfer', foreign_keys='transfer.c.target_wallet_id'
    )

    def __repr__(self):
        return f'<Wallet {self.user} {self.currency}>'


class Currency(Base):

    __tablename__ = 'currency'

    id = Column(
        Integer,
        primary_key=True,
    )
    code = Column(
        String(10),
        nullable=False,
        unique=True,
    )

    def __repr__(self):
        return f'<Currency {self.code}>'


class Transfer(Base):

    __tablename__ = 'transfer'

    id = Column(
        Integer,
        primary_key=True,
    )
    from_wallet_id = Column(
        Integer, ForeignKey('wallet.id'), nullable=True
    )  # if null then it was replenishment of the wallet
    target_wallet_id = Column(Integer, ForeignKey('wallet.id'))
    amount = Column(DECIMAL(12, 2), nullable=False)
    # database-side creating time
    event_time = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Transfer {self.amount} to {self.target_wallet}>'
