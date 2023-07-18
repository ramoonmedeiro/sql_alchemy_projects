import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from typing import Optional
from sqlalchemy.future.engine import Engine
from models.model_base import ModelBase

# env vars
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")


__engine: Optional[Engine] = None


def create_engine(sqlite: bool = False) -> Engine:

    global __engine

    if __engine:
        return

    if sqlite:
        arquivo_db = 'db/picoles.sqlite'
        folder = Path(arquivo_db).parent
        folder.mkdir(parents=True, exist_ok=True)

        conn_str = f'sqlite:///{arquivo_db}'
        __engine = sa.create_engine(
            url=conn_str,
            echo=False,
            connect_args={'check_same_thread': False}
            )

    else:
        conn_str = f'postgresql://{db_user}:{db_password}@localhost:5432/picoles'
        __engine = sa.create_engine(url=conn_str, echo=False)

    return __engine


def create_session() -> Session:

    global __engine

    if not __engine:
        __engine = create_engine(sqlite=False)

    __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    session: Session = __session()

    return session


def create_tables() -> None:

    global __engine

    if not __engine:
        __engine = create_engine(sqlite=False)

    import models.__all_models
    ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
