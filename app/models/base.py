from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """所有数据库模型的公共基类。"""

    # SQLAlchemy 会将继承这个类的模型登记到 Base.metadata。
    # 后续 Alembic 通过 metadata 了解我们定义了哪些表。
    pass