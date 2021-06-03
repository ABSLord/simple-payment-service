from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class UserInputSchema(BaseModel):
    username: str
    password: str


class UserResponseSchema(BaseModel):
    username: str


class LoginResponseSchema(BaseModel):
    access_token: str


class MeResponseSchema(BaseModel):
    username: str
    currency_code: str
    balance: Decimal


class ReceiveMoneyInputSchema(BaseModel):
    amount: Decimal


class ReceiveMoneyResponseSchema(BaseModel):
    balance: Decimal


class SendMoneyInputSchema(BaseModel):
    target_username: str
    amount: Decimal


class SendMoneyResponseSchema(BaseModel):
    balance: Decimal


class TransferType(str, Enum):
    incoming = 'incoming'
    outgoing = 'outgoing'


class TransferSchema(BaseModel):
    type: TransferType
    amount: Decimal
    transfer_time: datetime


class TransfersListResponseSchema(BaseModel):
    __root__: list[TransferSchema]
