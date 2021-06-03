from fastapi import APIRouter

from app.api.v1.transfers import transfer_router
from app.api.v1.users import user_router
from app.api.v1.wallets import wallet_router


api_v1_router = APIRouter()

api_v1_router.include_router(
    user_router,
    prefix='/users',
    tags=['users'],
)
api_v1_router.include_router(
    wallet_router,
    prefix='/wallets',
    tags=['wallets'],
)
api_v1_router.include_router(
    transfer_router,
    prefix='/transfers',
    tags=['transfers'],
)
