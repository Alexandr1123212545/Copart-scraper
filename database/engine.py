from typing import Annotated

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

sync_engine = create_engine(
    url = settings.db_url_psycopg,
    # echo=True,
    echo=False,
)

async_engine = create_async_engine(
    url = settings.db_url_asyncpg,
    # echo=True,
    echo=False,
)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

str_10 = Annotated[str, 10]
str_17 = Annotated[str, 17]
str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
str_100 = Annotated[str, 100]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_10: String(10),
        str_30: String(30),
        str_50: String(50),
        str_100: String(100)
    }
