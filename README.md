# Project Service

[![Python](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/)

## About

Service for managing projects and project related resources.

### Start

1. Install [Docker](https://www.docker.com/get-started/).
2. Start container with project application.

       docker compose up

3. Visit http://127.0.0.1:5064/v1/api-doc for API documentation.

### Development

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Install dependencies.

       poetry install

    2.1. For Mac Users:

        brew install libmagic


3. Add environment variables into `.env`.
4. Run application.

       poetry run python -m project

5. Generate migration (based on comparison of database to defined models).

       docker compose run --rm alembic revision --autogenerate -m "Migration message" --rev-id 0002 --depends-on 0001

## Acknowledgements

The development of the HealthDataCloud open source software was supported by the EBRAINS research infrastructure, funded from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3) and H2020 Research and Innovation Action Grant Interactive Computing E-Infrastructure for the Human Brain Project ICEI 800858.

This project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101058516. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or other granting authorities. Neither the European Union nor other granting authorities can be held responsible for them.

![HDC-EU-acknowledgement](https://hdc.humanbrainproject.eu/img/HDC-EU-acknowledgement.png)
