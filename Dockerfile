FROM python:3.7-alpine

WORKDIR /usr/src/coins_wallet_service

RUN pip install poetry && poetry config settings.virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-interaction

COPY . ./

COPY coins_wallet_service/settings.py ./coins_wallet_service/settings.py

EXPOSE 8000

ENTRYPOINT ["./docker/entrypoint.sh"]
