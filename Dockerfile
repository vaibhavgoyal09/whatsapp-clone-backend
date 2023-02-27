FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - 

# Copy using poetry.lock* in case it doesn't exist yet
COPY ["app/", "data/", "domain/", "poetry.lock", "pyproject.toml", "firebase-adminsdk.json", ".env"] /app/

WORKDIR /app

RUN poetry install

CMD ["uvicorn" "app.main:app" "--host" "0.0.0.0" "--port", "8000"]
