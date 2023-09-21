# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from pydantic import BaseModel

from project.components.models import ModelList


class TestModelList:
    def test_map_by_field_returns_map_based_on_field_argument_as_key(self, fake):
        class Model(BaseModel):
            id: int

        model_1 = Model(id=fake.pyint())
        model_2 = Model(id=fake.pyint())

        models = ModelList([model_1, model_2])

        expected_map = {
            str(model_1.id): model_1,
            str(model_2.id): model_2,
        }

        assert models.map_by_field('id', str) == expected_map
