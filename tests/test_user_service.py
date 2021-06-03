import pytest
from sqlalchemy.future import select

from app.models import Currency, User, Wallet
from app.services.users import UserNotFound, UserService
from app.settings import DEFAULT_CURRENCY_CODE
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio()
async def test_create_user_with_wallet():
    test_username = 'test_user'
    test_password = '123'
    async with TestingSessionLocal() as session:

        with pytest.raises(UserNotFound):
            await UserService(session).get_by_username(test_username)

        await UserService(session).create_with_wallet(test_username, test_password)

        all_users = (await session.execute(select(User))).scalars().all()

        assert len(all_users) == 1
        assert all_users[0].username == test_username

        all_wallets = (await session.execute(select(Wallet))).scalars().all()

        assert len(all_wallets) == 1
        assert all_wallets[0].user_id == all_users[0].id

        all_currencies = (await session.execute(select(Currency))).scalars().all()

        assert len(all_currencies) == 1
        assert all_currencies[0].code == DEFAULT_CURRENCY_CODE
        assert all_wallets[0].currency_id == all_currencies[0].id
