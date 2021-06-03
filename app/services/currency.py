from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.future import select

from app.models import Currency
from app.services.base import BaseService
from app.settings import DEFAULT_CURRENCY_CODE


class CurrencyService(BaseService):
    async def get_or_create_default(self):
        # emulate get_or_create behavior from django orm
        get_stmt = select(Currency).filter(Currency.code == DEFAULT_CURRENCY_CODE)
        try:
            return (await self._session.execute(get_stmt)).scalar_one()
        except NoResultFound:
            try:
                async with self._session.begin_nested():
                    self._session.add(Currency(code=DEFAULT_CURRENCY_CODE))
            except IntegrityError:
                pass
            finally:
                return (await self._session.execute(get_stmt)).scalar_one()
