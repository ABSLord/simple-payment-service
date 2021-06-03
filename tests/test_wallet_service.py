from decimal import Decimal

import pytest
from sqlalchemy.future import select

from app.models import Transfer, Wallet
from app.services.users import UserService
from app.services.wallets import (
    AmountMustBePositive,
    NotEnoughMoneyException,
    WalletService,
)
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio()
async def test_receive_money():
    async with TestingSessionLocal() as session:
        await UserService(session).create_with_wallet('test_user', '123')
        wallet = (await session.execute(select(Wallet))).scalars().first()

        assert wallet.balance == Decimal(0)

        await WalletService(session).receive_money(wallet.id, Decimal(10))
        transfers = (await session.execute(select(Transfer))).scalars().all()
        wallet = (await session.execute(select(Wallet))).scalars().first()

        assert wallet.balance == Decimal(10)
        assert len(transfers) == 1
        assert transfers[0].from_wallet_id is None
        assert transfers[0].target_wallet_id == wallet.id
        assert transfers[0].amount == Decimal(10)

        with pytest.raises(AmountMustBePositive):
            await WalletService(session).receive_money(wallet.id, Decimal(-10))
        wallet = (await session.execute(select(Wallet))).scalars().first()

        assert wallet.balance == Decimal(10)


@pytest.mark.asyncio()
async def test_send_money():
    first_username = 'first_user'
    second_username = 'second_user'
    test_password = '123'
    async with TestingSessionLocal() as session:
        await UserService(session).create_with_wallet(first_username, test_password)
        await UserService(session).create_with_wallet(second_username, test_password)
        all_wallets = (await session.execute(select(Wallet))).scalars().all()
        first_wallet_id = all_wallets[0].id
        second_wallet_id = all_wallets[1].id
        await WalletService(session).receive_money(first_wallet_id, Decimal(10))
        await WalletService(session).send_money(
            first_wallet_id, second_wallet_id, Decimal(10)
        )
        updated_first_wallet = await session.get(Wallet, first_wallet_id)
        updated_second_wallet = await session.get(Wallet, second_wallet_id)
        assert updated_first_wallet.balance == Decimal(0)
        assert updated_second_wallet.balance == Decimal(10)
        with pytest.raises(NotEnoughMoneyException):
            await WalletService(session).send_money(
                first_wallet_id, second_wallet_id, Decimal(10)
            )
