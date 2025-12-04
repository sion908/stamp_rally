# flake8: noqa: F800
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# from database.base import Base  # モデルクラスの読み込み
# from database.base import User  # モデルクラスの読み込み

from database.base_class import Base  # noqa:E402
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from database.db import DB_URL  # DBの接続情報をimport  # noqa:E402
from models import *  # noqa:F401,E402,F403

target_metadata = Base.metadata  # db/base.pyで定義したBaseクラスのメタデータを使用
# target_metadata = User.metadata # db/base.pyで定義したBaseクラスのメタデータを使用

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        # literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# https://alembic.sqlalchemy.org/en/latest/autogenerate.html#affecting-the-rendering-of-types-themselves
def render_item(type_, obj, autogen_context):
    """Apply rendering for custom sqlalchemy types"""
    if type_ == "type":
        module_name = obj.__class__.__module__
        if module_name.startswith("sqlalchemy_utils."):
            return render_sqlalchemy_utils_type(obj, autogen_context)

    # render default
    return False


def render_sqlalchemy_utils_type(obj, autogen_context):
    class_name = obj.__class__.__name__
    import_statement = f"from sqlalchemy_utils.types import {class_name}"
    autogen_context.imports.add(import_statement)
    if class_name == 'ChoiceType':
        return render_choice_type(obj, autogen_context)
    return f"{class_name}()"


def render_choice_type(obj, autogen_context):
    choices = obj.choices
    if obj.type_impl.__class__.__name__ == 'EnumTypeImpl':
        choices = obj.type_impl.enum_class.__name__
        import_statement = f"from models import {choices}"
        autogen_context.imports.add(import_statement)
    impl_stmt = f"sa.{obj.impl.__class__.__name__}()"
    return f"{obj.__class__.__name__}(choices={choices}, impl={impl_stmt})"


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_item=render_item
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    conf = config.get_section(config.config_ini_section)  # alembic.iniの読み込み

    # sqlalchemy.urlをdb/db.pyからimportした接続情報で上書き
    if not conf.get("sqlalchemy.url"):
        conf["sqlalchemy.url"] = DB_URL

    connectable = async_engine_from_config(
        conf,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        trans = await connection.begin()  # トランザクション開始
        try:
            await connection.run_sync(do_run_migrations)
            await trans.commit()  # コミット
        except Exception as e:
            await trans.rollback()  # ロールバック
            print(f"Migration failed: {e}")
            raise
        finally:
            await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
