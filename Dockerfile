FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

WORKDIR /home/app
RUN mkdir -p /home/app/.database

COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install poetry
RUN poetry install

COPY . ./

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
