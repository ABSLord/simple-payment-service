from typing import Any, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models import Base


EntityT = TypeVar('EntityT', bound=Base)


class BaseService:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def get_stmt_creator(
        entity: EntityT, filters: Optional[list] = None, joins: Optional[list[str]] = None
    ) -> Any:
        get_stmt = select(entity)
        if filters:
            get_stmt = get_stmt.filter(*filters)
        if joins:
            get_stmt = get_stmt.options(*[joinedload(join) for join in joins])
        return get_stmt
