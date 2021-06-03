from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import TransfersListResponseSchema, TransferType
from app.services.transfers import TransferService
from app.services.users import UserNotFound, UserService


transfer_router = APIRouter()


@transfer_router.get('/', response_model=TransfersListResponseSchema)
async def get_all(
    auth: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
):
    auth.jwt_required()
    current_username = auth.get_jwt_subject()
    try:
        current_user = await UserService(session).get_by_username(
            current_username, joins=['wallet']
        )
    except UserNotFound as exc:
        raise HTTPException(400, detail=str(exc))
    transfer_history = await TransferService(session).get_all(current_user.wallet.id)

    return TransfersListResponseSchema.parse_obj(
        [
            {
                'transfer_time': obj.event_time,
                'amount': obj.amount,
                'type': TransferType.outgoing
                if obj.from_wallet_id == current_user.wallet.id
                else TransferType.incoming,
            }
            for obj in transfer_history
        ]
    )
