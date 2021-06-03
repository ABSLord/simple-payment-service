from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import (
    ReceiveMoneyInputSchema,
    ReceiveMoneyResponseSchema,
    SendMoneyInputSchema,
    SendMoneyResponseSchema,
)
from app.services.users import UserNotFound, UserService
from app.services.wallets import (
    AmountMustBePositive,
    NotEnoughMoneyException,
    WalletNotFound,
    WalletService,
)
from app.utils import check_idempotency


wallet_router = APIRouter()


@wallet_router.patch('/receive', response_model=ReceiveMoneyResponseSchema)
async def receive_money(
    receive_money_info: ReceiveMoneyInputSchema,
    auth: AuthJWT = Depends(),
    x_idempotency_key: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    is_idempotent_request = await check_idempotency(x_idempotency_key)
    if not is_idempotent_request:
        raise HTTPException(
            400, detail='Duplicate request, check x-idempotency-key header!'
        )
    auth.jwt_required()
    current_username = auth.get_jwt_subject()
    try:
        current_user = await UserService(session).get_by_username(
            current_username, joins=['wallet']
        )
    except UserNotFound as exc:
        raise HTTPException(400, detail=str(exc))
    try:
        updated_wallet = await WalletService(session).receive_money(
            current_user.wallet.id, receive_money_info.amount
        )
    except WalletNotFound as exc:
        # todo: may be create wallet instead of raising error
        raise HTTPException(400, detail=str(exc))
    except AmountMustBePositive:
        raise HTTPException(400, detail='Amount must be positive')

    return ReceiveMoneyResponseSchema(balance=updated_wallet.balance)


@wallet_router.patch('/send', response_model=SendMoneyResponseSchema)
async def send_money(
    send_money_info: SendMoneyInputSchema,
    auth: AuthJWT = Depends(),
    x_idempotency_key: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    is_idempotent_request = await check_idempotency(x_idempotency_key)
    if not is_idempotent_request:
        raise HTTPException(
            400, detail='Duplicate request, check x-idempotency-key header!'
        )
    auth.jwt_required()
    current_username = auth.get_jwt_subject()
    try:
        current_user = await UserService(session).get_by_username(
            current_username, joins=['wallet']
        )
        target_user = await UserService(session).get_by_username(
            send_money_info.target_username, joins=['wallet']
        )
    except UserNotFound as exc:
        raise HTTPException(400, detail=str(exc))
    try:
        current_user_wallet = await WalletService(session).send_money(
            current_user.wallet.id, target_user.wallet.id, send_money_info.amount
        )
    except NotEnoughMoneyException as exc:
        raise HTTPException(400, detail=str(exc))
    except WalletNotFound as exc:
        # todo: may be create wallet instead of raising error
        raise HTTPException(400, detail=str(exc))
    except AmountMustBePositive:
        raise HTTPException(400, detail='Amount must be positive')

    return SendMoneyResponseSchema(balance=current_user_wallet.balance)
