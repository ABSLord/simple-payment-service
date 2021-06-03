from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import (
    LoginResponseSchema,
    MeResponseSchema,
    UserInputSchema,
    UserResponseSchema,
)
from app.services.users import UserAlreadyExists, UserNotFound, UserService
from app.utils import check_password


user_router = APIRouter()


@user_router.post('/', response_model=UserResponseSchema)
async def create(user: UserInputSchema, session: AsyncSession = Depends(get_session)):
    try:
        created_user = await UserService(session).create_with_wallet(
            user.username, user.password
        )
    except UserAlreadyExists as exc:
        raise HTTPException(400, detail=str(exc))
    return UserResponseSchema(username=created_user.username)


@user_router.post('/login', response_model=LoginResponseSchema)
async def login(
    user: UserInputSchema,
    auth: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_session),
):
    try:
        db_user = await UserService(session).get_by_username(user.username)
    except UserNotFound as exc:
        raise HTTPException(400, detail=str(exc))
    if not check_password(db_user.password, user.password):
        raise HTTPException(401, detail='Invalid credentials')
    access_token = auth.create_access_token(subject=user.username)
    return LoginResponseSchema(access_token=access_token)


@user_router.get('/me', response_model=MeResponseSchema)
async def me(auth: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)):
    auth.jwt_required()
    current_user = auth.get_jwt_subject()
    user = await UserService(session).get_by_username(
        current_user, joins=['wallet', 'wallet.currency']
    )
    me_info = MeResponseSchema(
        **{
            'username': user.username,
            'balance': user.wallet.balance,
            'currency_code': user.wallet.currency.code,
        }
    )
    return me_info
