# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.workbench.crud import WorkbenchCRUD
from project.dependencies import get_db_session


def get_workbench_crud(db_session: AsyncSession = Depends(get_db_session)) -> WorkbenchCRUD:
    """Return an instance of WorkbenchCRUD as a dependency."""

    return WorkbenchCRUD(db_session)
