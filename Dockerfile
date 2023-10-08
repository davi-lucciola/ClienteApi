FROM python:3.11.4-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /user-api

COPY poetry.lock pyproject.toml /user-api/

RUN pip3 install --upgrade pip &&\
    pip3 install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install 

COPY . /user-api/

EXPOSE 8000

CMD ["uvicorn", "app.main:user_api", "--host", "0.0.0.0", "--port", "8000", "--reload"]
