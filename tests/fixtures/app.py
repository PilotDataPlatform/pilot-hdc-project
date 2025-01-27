# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio
from asyncio import AbstractEventLoop
from contextlib import AbstractContextManager
from typing import Any
from typing import Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from project.app import create_app
from project.config import Settings
from project.config import get_settings
from project.dependencies import get_db_session


class OverrideDependencies(AbstractContextManager):
    """Temporarily override application dependencies using context manager."""

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.stashed_dependencies = {}
        self.dependencies_to_override = {}

    def __call__(self, dependencies: dict[Callable[..., Any], Callable[..., Any]]) -> 'OverrideDependencies':
        self.dependencies_to_override = dependencies
        return self

    def __enter__(self) -> 'OverrideDependencies':
        self.stashed_dependencies = self.app.dependency_overrides.copy()
        self.app.dependency_overrides.update(self.dependencies_to_override)
        return self

    def __exit__(self, *args: Any) -> None:
        self.app.dependency_overrides.clear()
        self.app.dependency_overrides.update(self.stashed_dependencies)
        self.dependencies_to_override = {}
        return None


@pytest.fixture
def override_dependencies(app) -> OverrideDependencies:
    yield OverrideDependencies(app)


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def settings(db_port) -> Settings:
    settings = Settings(
        RDS_DB_USERNAME='test',
        RDS_DB_PASSWORD='test',
        RDS_DB_NAME='test',
        RDS_DB_PORT=db_port,
        S3_ACCESS_KEY='test',
        S3_SECRET_KEY='testtest',
    )
    yield settings


@pytest.fixture
def app(event_loop, settings, db_session) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    app.dependency_overrides[get_db_session] = lambda: db_session
    yield app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url='https://project') as client:
        yield client


@pytest.fixture
def non_mocked_hosts() -> list:
    return ['project', '127.0.0.1']
