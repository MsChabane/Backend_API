from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import  async_sessionmaker,create_async_engine
from App.config import config
from redis.asyncio import Redis


engine = create_async_engine(config.DATABASE_URL)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

redis = Redis(
    host='localhost',
    db=0
)


async def init_db():
    async with engine.begin() as conn:
        from App.models.User import User 
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session