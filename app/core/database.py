from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# engine 管理数据库连接池，供整个应用复用。
# 创建 engine 时不会立即连接数据库，获取连接或执行查询时才会通信。
engine = create_async_engine(
    settings.database_url.get_secret_value(),  # 取出 SecretStr 中的连接地址
    pool_pre_ping=True,                        # 复用连接前检查它是否仍然可用
    connect_args={"timeout": 5},               # asyncpg 建立连接的超时时间，单位为秒
)


# 会话工厂：统一配置，按需创建独立的 AsyncSession。
# expire_on_commit=False：提交后不自动将 ORM 对象属性标记为过期。
session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """向 FastAPI 请求提供独立的数据库会话，并负责清理。"""

    # 每次调用创建一个会话，避免并发请求共享同一个 Session。
    async with session_factory() as session:
        # FastAPI 将这里的 session 注入需要它的接口。
        yield session

    # 离开 async with 时关闭会话、释放它持有的连接。
    # 不会关闭整个连接池，也不会自动提交业务修改。