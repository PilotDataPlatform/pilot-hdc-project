# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from project.components.crud import CRUD
from project.components.workbench.models import Workbench


class WorkbenchCRUD(CRUD):
    """CRUD for managing workbench database models."""

    model = Workbench
