from aiocache import caches
from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config


config = Config()

DEBUG = config('DEBUG', cast=bool, default=False)
RELOAD = config('RELOAD', cast=bool, default=False)
APP_HOST = config('APP_HOST', cast=str, default='0.0.0.0')
APP_PORT = config('APP_PORT', cast=int, default=8888)

DATABASE = {
    'username': config('DB_USER', default='developer'),
    'password': config('DB_PASSWORD', default='123'),
    'host': config('DB_HOST', default='0.0.0.0'),
    'port': config('DB_PORT', cast=int, default=5432),
    'database': config('DB_NAME', default='simplepaymentservice'),
}

ASYNC_DB_DSN = config(
    'ASYNC_DB_DSN',
    cast=make_url,
    default=URL.create(drivername='postgresql+asyncpg', **DATABASE),
)

SYNC_DB_DSN = config(
    'SYNC_DB_DSN',
    cast=make_url,
    default=URL.create(drivername='postgresql', **DATABASE),
)

TEST_DB_DSN = 'sqlite+aiosqlite:///./tests/test.db'

DEFAULT_CURRENCY_CODE = 'USD'

# in-memory default cache
# add memcached/redis cache if needed
caches.set_config(
    {
        'default': {
            'cache': 'aiocache.SimpleMemoryCache',
            'serializer': {'class': 'aiocache.serializers.StringSerializer'},
        },
    }
)

CACHE_BACKEND = config('CACHE_BACKEND', cast=str, default='default')

AUTH_SECRET_KEY = config('AUTH_SECRET_KEY', cast=str, default='secret')
