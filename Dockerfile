FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.13

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc python3-dev musl-dev netcat

RUN pip install "poetry==$POETRY_VERSION"

COPY ./poetry.lock ./pyproject.toml /app/

RUN poetry run pip install -U pip \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . .

ENTRYPOINT ["./entrypoint.sh"]

#EXPOSE 8000
