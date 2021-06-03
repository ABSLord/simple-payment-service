import uvicorn

from app import settings
from app.application import create_app


APP = create_app()

if __name__ == '__main__':
    uvicorn.run(
        '__main__:APP',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.DEBUG,
        reload=settings.RELOAD,
    )
