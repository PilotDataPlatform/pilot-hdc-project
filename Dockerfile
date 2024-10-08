FROM docker-registry.ebrains.eu/hdc-services-image/base-image:python-3.10.14-v1 AS production-environment

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction


FROM production-environment AS project-image

COPY project ./project

RUN chown -R app:app /app
USER app

ENTRYPOINT ["python3", "-m", "project"]


FROM production-environment AS development-environment

RUN poetry install --no-root --no-interaction


FROM development-environment AS alembic-image

ENV ALEMBIC_CONFIG=migrations/alembic.ini

COPY project ./project
COPY migrations ./migrations

RUN chown -R app:app /app
USER app

ENTRYPOINT ["python3", "-m", "alembic"]

CMD ["upgrade", "head"]
