FROM python:3.11.4-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /user-api

COPY poetry.lock pyproject.toml /user-api/

RUN apk update &&\
    apk add python3-dev libpq-dev&&\
    pip3 install --upgrade pip &&\
    pip3 install --no-cache-dir poetry==1.3.2 &&\
    poetry config virtualenvs.create false &&\
    poetry install 

COPY . /user-api/

EXPOSE 8000

CMD ["uvicorn", "api.main:user_api", "--host", "0.0.0.0", "--port", "8000", "--reload"]
