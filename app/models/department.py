from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Department(Base):
    """部门模型，每条记录代表一个部门。"""

    # 指定实际数据库表名。
    __tablename__ = "departments"

    # 防止部门名称为空字符串或只有空格。
    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_departments_name_not_blank",
        ),
    )

    # 主键唯一标识部门。
    # 传 uuid4 函数，而不是 uuid4()，让每次插入分别生成 UUID。
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    # 部门名称必填、最长 100 个字符，数据库中不能重复。
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    # 创建时间由数据库在插入记录时生成，保存带时区的时间。
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )