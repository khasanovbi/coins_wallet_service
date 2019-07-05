FROM python:3.7-alpine

WORKDIR /usr/src/coins_wallet_service

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install poetry && poetry config settings.virtualenvs.create false \
    && pip install gunicorn

COPY poetry.lock pyproject.toml ./

ARG install_dev=false
RUN poetry install $([ "$install_dev" == "false" ] && echo "--no-dev") --no-interaction

COPY . ./

EXPOSE 8000

CMD ["gunicorn", "coins_wallet_service.wsgi:application", "--bind=0.0.0.0:8000", \
    "--log-level=debug", "--workers=4"]
