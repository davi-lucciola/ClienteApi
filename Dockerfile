FROM python:3.11-alpine

WORKDIR /user-api

COPY poetry.lock pyproject.toml /user-api/

RUN pip3 install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install 

COPY . /user-api/

EXPOSE 8000

CMD ["uvicorn", "app.main:user_api", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--reload"]
