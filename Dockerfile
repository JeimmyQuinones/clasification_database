FROM python:3.12

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN bash -c "poetry install --no-root --only main "

ENV PYTHONPATH=/app

COPY ./alembic.ini /app/

COPY ./prestart.sh /app
COPY ./api /app/api

CMD ["./prestart.sh"]