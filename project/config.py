# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional

from common import VaultClient
from pydantic import BaseSettings
from pydantic import Extra
from pydantic import Field
from pydantic import HttpUrl


class VaultConfig(BaseSettings):
    """Store vault related configuration."""

    APP_NAME: str = 'project'
    CONFIG_CENTER_ENABLED: bool = False

    VAULT_URL: Optional[str] = None
    VAULT_CRT: Optional[str] = None
    VAULT_TOKEN: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    config = VaultConfig()

    if not config.CONFIG_CENTER_ENABLED:
        return {}

    client = VaultClient(config.VAULT_URL, config.VAULT_CRT, config.VAULT_TOKEN)
    return client.get_from_vault(config.APP_NAME)


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'project'
    VERSION: str = '2.1.0'
    HOST: str = '127.0.0.1'
    PORT: int = 5064
    WORKERS: int = 1

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    RDS_DB_HOST: str = Field('127.0.0.1', env={'RDS_DB_HOST', 'OPSDB_UTILITY_HOST'})
    RDS_DB_PORT: int = Field(6432, env={'RDS_DB_PORT', 'OPSDB_UTILITY_PORT'})
    RDS_DB_USERNAME: str = Field('postgres', env={'RDS_DB_USERNAME', 'OPSDB_UTILITY_USERNAME'})
    RDS_DB_PASSWORD: str = Field('postgres-project-pilot', env={'RDS_DB_PASSWORD', 'OPSDB_UTILITY_PASSWORD'})
    RDS_DB_NAME: str = 'project'
    RDS_ECHO_SQL_QUERIES: bool = False

    S3_HOST: str = '127.0.0.1'
    S3_PORT: int = 9100
    S3_HTTPS_ENABLED: bool = False
    S3_GATEWAY_ENABLED: bool = False
    S3_ACCESS_KEY: str = Field('ACCESSKEY/GMIMPKTWGOKHIQYYQHPO', env={'S3_ACCESS_KEY', 'MINIO_ACCESS_KEY'})
    S3_SECRET_KEY: str = Field('SECRETKEY/HJGKVAS/TRglfFvzDrbYpdknbc', env={'S3_SECRET_KEY', 'MINIO_SECRET_KEY'})
    S3_BUCKET_ENCRYPTION_ENABLED: bool = False
    S3_BUCKET_ZONE_PREFIXES: list[str] = ['gr', 'core']
    S3_BUCKET_FOR_PROJECT_LOGOS: str = 'project-logos'
    S3_PREFIX_FOR_PROJECT_IMAGE_URLS: HttpUrl = 'http://127.0.0.1:9100/project-logos'

    OPEN_TELEMETRY_ENABLED: bool = False
    OPEN_TELEMETRY_HOST: str = '127.0.0.1'
    OPEN_TELEMETRY_PORT: int = 6831

    METADATA_SERVICE: HttpUrl = 'http://metadata.utility'
    AUTH_SERVICE: HttpUrl = 'http://auth.utility'

    ICON_SIZE_LIMIT: int = 2**24

    SERVICE_CLIENT_TIMEOUT: int = 5

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return init_settings, env_settings, load_vault_settings, file_secret_settings

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

        self.RDS_DB_URI = (
            f'postgresql+asyncpg://{self.RDS_DB_USERNAME}:{self.RDS_DB_PASSWORD}'
            f'@{self.RDS_DB_HOST}:{self.RDS_DB_PORT}/{self.RDS_DB_NAME}'
        )
        s3_protocol = 'https' if self.S3_HTTPS_ENABLED else 'http'
        self.S3_ENDPOINT_URL = f'{s3_protocol}://{self.S3_HOST}:{self.S3_PORT}'


@lru_cache(1)
def get_settings() -> Settings:
    settings = Settings()
    return settings
