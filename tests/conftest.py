# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

pytest_plugins = [
    'tests.fixtures.components.project',
    'tests.fixtures.components.resource_request',
    'tests.fixtures.components.workbench',
    'tests.fixtures.app',
    'tests.fixtures.db',
    'tests.fixtures.fake',
    'tests.fixtures.jq',
    'tests.fixtures.s3',
    'tests.fixtures.policy',
]
