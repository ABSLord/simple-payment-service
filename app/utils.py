import hashlib

from aiocache import caches

from app.settings import CACHE_BACKEND


def get_hashed_password(password: str):
    return hashlib.sha512(password.encode()).hexdigest()


def check_password(hashed_password: str, password_to_check: str):
    return hashed_password == get_hashed_password(password_to_check)


async def check_idempotency(idempotency_key: str):
    cache = caches.get(CACHE_BACKEND)
    cached_value = await cache.get(idempotency_key, None)
    if cached_value is None:
        await cache.set(idempotency_key, 'ok')
    return cached_value is None
