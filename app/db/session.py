from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.settings import settings

engine = create_async_engine(settings.database.url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
