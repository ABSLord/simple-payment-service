from typing import Optional

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.models import User
from app.services.base import BaseService
from app.services.wallets import WalletService
from app.utils import get_hashed_password


class UserServiceException(Exception):
    pass


class UserAlreadyExists(UserServiceException):
    pass


class UserNotFound(UserServiceException):
    pass


class UserService(BaseService):
    async def create_with_wallet(self, username: str, password: str):
        stmt = insert(User).values(
            username=username, password=get_hashed_password(password)
        )
        try:
            await self._session.execute(stmt)

            new_user = await self.get_by_username(username)
            await WalletService(self._session).create_wallet_with_default_currency(
                new_user.id, need_commit=False
            )
            await self._session.commit()
        except IntegrityError:
            raise UserAlreadyExists(f'User with username {username} already exists')
        except Exception as exc:
            raise UserServiceException(str(exc))
        return new_user

    async def get_by_id(self, user_id: int, joins: Optional[list[str]] = None):
        try:
            get_stmt = self.get_stmt_creator(
                User,
                [
                    User.id == user_id,
                ],
                joins,
            )
            return (await self._session.execute(get_stmt)).scalars().one()
        except NoResultFound:
            raise UserNotFound(f'User with user_id {user_id} not found')

    async def get_by_username(self, username: str, joins: Optional[list[str]] = None):
        try:
            get_stmt = self.get_stmt_creator(
                User,
                [
                    User.username == username,
                ],
                joins,
            )
            return (await self._session.execute(get_stmt)).scalars().one()
        except NoResultFound:
            raise UserNotFound(f'User with username {username} not found')
