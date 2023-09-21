# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from faker import Faker

from project.components.crud import CRUD


class BaseFactory:
    """Base class for creating testing purpose entries."""

    crud: CRUD
    fake: Faker

    def __init__(self, crud: CRUD, fake: Faker) -> None:
        self.crud = crud
        self.fake = fake
