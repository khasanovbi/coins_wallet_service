FROM python:3.7-alpine

WORKDIR /usr/src/coins_wallet_service

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install poetry && poetry config settings.virtualenvs.create false \
    && pip install gunicorn

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-interaction

COPY . ./

EXPOSE 8000

CMD ["docker/entrypoint.sh"]
