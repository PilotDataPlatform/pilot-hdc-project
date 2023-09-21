# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from project.components.resource_request.models import ResourceRequest
from project.components.resource_request.views import router as resource_request_router

__all__ = [
    'ResourceRequest',
    'resource_request_router',
]
