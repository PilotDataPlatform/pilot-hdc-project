# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from base64 import b64encode
from io import BytesIO

import faker
import pytest
from PIL import Image


class Faker(faker.Faker):
    def image(self, size: tuple[int, int] = (512, 512), format_type: str = 'PNG') -> bytes:
        """Generate an image."""

        buffer = BytesIO()
        color = self.color(hue='red')
        image = Image.new('RGB', size, color)
        image.save(buffer, format_type)

        return buffer.getvalue()

    def base64_image(self, size: tuple[int, int] = (512, 512), format_type: str = 'PNG') -> str:
        """Generate an image as base64 string."""

        image = self.image(size, format_type)

        return b64encode(image).decode()


@pytest.fixture
def fake() -> Faker:
    yield Faker()
