# from sqlalchemy import Boolean, Column, Integer, String  # noqa:E800
# from sqlalchemy.orm.decl_api import declarative_base  # noqa:E800
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# from sqlalchemy.orm import relationship  # noqa:E800
# from sqlalchemy.sql.sqltypes import DateTime  # noqa:E800

# from .db import async_session  # noqa:E800

# Base = declarative_base()  # noqa:E800
# Base.query = async_session.query_property()  # noqa:E800


@as_declarative()
class Base:
    @declared_attr
    def __table_args__(self):  # noqa:U100
        return ({'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_bin'},)  # noqa:E501,E800

    @declared_attr
    def __tablename__(self):  # noqa:U100
        return self.__name__.lower()
