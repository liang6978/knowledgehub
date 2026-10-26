import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session


# 使用当前模块名创建日志记录器，便于定位错误来自哪个模块。
logger = logging.getLogger(__name__)

# 定义一组路由，main.py 会为它们统一添加 /api/v1 前缀。
router = APIRouter()


@router.get("/health")
async def health_check():
    """检查 HTTP 应用能否响应，不访问数据库。"""
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check(
    # Depends 告诉 FastAPI 调用 get_db_session 获取会话。
    # session 由后端提供，不是客户端需要填写的请求参数。
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """通过实际查询，检查数据库当前是否可访问。"""

    try:
        # text() 将 SQL 字符串包装成 SQLAlchemy 可执行的语句。
        # await 等待查询完成；SELECT 1 不读取或修改业务数据。
        await session.execute(text("SELECT 1"))

    except (SQLAlchemyError, OSError, TimeoutError):
        # 在服务端日志保留错误堆栈，便于排查。
        logger.exception("Database readiness check failed")

        # 对客户端返回稳定的错误信息，不暴露数据库内部详情。
        # 503 表示服务暂时无法就绪。
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from None

    return {"status": "ready"}