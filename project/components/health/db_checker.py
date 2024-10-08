# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.logger import logger


class DBChecker:
    """Perform checks against the database."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def is_online(self) -> bool:
        """Check if database is online."""

        try:
            cursor = await self.session.execute(select(1))
            result = cursor.scalars().first()
            return result == 1
        except Exception:
            logger.exception('An exception occurred while performing database query.')

        return False
