# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import os
from contextlib import contextmanager
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from testcontainers.postgres import PostgresContainer

POSTGRES_DOCKER_IMAGE = 'postgres:14.2-alpine'


@contextmanager
def chdir(directory: Path) -> None:
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


@pytest.fixture(scope='session')
def project_root() -> Path:
    path = Path(__file__)

    while path.name != 'project':
        path = path.parent

    yield path


@pytest.fixture(scope='session')
def db_port(project_root) -> str:
    with PostgresContainer(image=POSTGRES_DOCKER_IMAGE) as pg_container:
        database_uri = pg_container.get_connection_url()

        config = Config('migrations/alembic.ini')
        with chdir(project_root):
            config.set_main_option('database_uri', database_uri)
            upgrade(config, 'head')

        yield pg_container.get_exposed_port(pg_container.port_to_expose)


@pytest.fixture(scope='session')
def db_engine(settings) -> AsyncEngine:
    yield create_async_engine(settings.RDS_DB_URI, echo=settings.RDS_ECHO_SQL_QUERIES)


@pytest.fixture
async def db_session(db_engine) -> AsyncSession:
    session = AsyncSession(bind=db_engine, expire_on_commit=False)

    try:
        yield session
    finally:
        await session.close()
