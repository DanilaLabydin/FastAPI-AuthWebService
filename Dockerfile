FROM python:3.10-slim

RUN mkdir -m 777 /app

RUN pip install poetry==1.3.2
COPY ./src/database.ini ./src/.env poetry.lock pyproject.toml /app/

WORKDIR /app/

COPY . .

RUN poetry --no-root install

# RUN pip install -r requirements.txt
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]