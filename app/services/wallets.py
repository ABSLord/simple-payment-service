from decimal import Decimal

from sqlalchemy import insert

from app.models import Transfer, Wallet
from app.services.base import BaseService
from app.services.currency import CurrencyService


class WalletServiceException(Exception):
    pass


class WalletNotFound(WalletServiceException):
    pass


class AmountMustBePositive(WalletServiceException):
    pass


class NotEnoughMoneyException(WalletServiceException):
    pass


class WalletService(BaseService):
    async def create_wallet_with_default_currency(
        self, user_id: int, need_commit: bool = False
    ):
        """Create wallet with default currency(from settings) for user"""
        default_currency = await CurrencyService(self._session).get_or_create_default()
        stmt = insert(Wallet).values(
            user_id=user_id, currency_id=default_currency.id, balance=0
        )
        await self._session.execute(stmt)
        if need_commit:
            await self._session.commit()

    async def receive_money(self, target_wallet_id: int, amount: Decimal):
        """
        Replenishment of your own wallet
        """
        if amount <= Decimal(0):
            raise AmountMustBePositive()
        # get row and lock it for update
        obj_target = await self._session.get(
            Wallet,
            target_wallet_id,
            populate_existing=True,
            with_for_update={'nowait': False},
        )
        if not obj_target:
            raise WalletNotFound()
        obj_target.balance += amount
        stmt = insert(Transfer).values(
            target_wallet_id=target_wallet_id,
            amount=amount,
        )
        await self._session.execute(stmt)
        #  save all in single transaction
        await self._session.commit()
        return obj_target

    async def send_money(
        self, from_wallet_id: int, target_wallet_id: int, amount: Decimal
    ):
        """
        Transfer from your wallet to another user's wallet
        """
        if amount <= Decimal(0):
            raise AmountMustBePositive()
        obj_from = await self._session.get(
            Wallet,
            from_wallet_id,
            populate_existing=True,
            with_for_update={'nowait': False},
        )
        if obj_from and obj_from.balance < amount:
            # rollback for unlock row
            await self._session.rollback()
            raise NotEnoughMoneyException('There is not enough money in your wallet')
        obj_target = await self._session.get(
            Wallet,
            target_wallet_id,
            populate_existing=True,
            with_for_update={'nowait': False},
        )
        if not (obj_from and obj_target):
            await self._session.rollback()
            raise WalletNotFound()
        obj_from.balance -= amount
        obj_target.balance += amount
        stmt = insert(Transfer).values(
            from_wallet_id=from_wallet_id,
            target_wallet_id=target_wallet_id,
            amount=amount,
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return obj_from
