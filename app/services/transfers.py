from sqlalchemy import or_

from app.models import Transfer
from app.services.base import BaseService


class TransferService(BaseService):
    async def get_all(self, wallet_id: int):
        get_stmt = self.get_stmt_creator(
            Transfer,
            [
                or_(
                    Transfer.from_wallet_id == wallet_id,
                    Transfer.target_wallet_id == wallet_id,
                ),
            ],
        )

        return (await self._session.execute(get_stmt)).scalars().all()
