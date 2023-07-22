FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY diploma-frontend-0.7.tar.gz diploma-frontend-0.7.tar.gz

RUN pip install --upgrade pip
RUN pip install 'poetry==1.5.1'
RUN poetry config virtualenvs.create false --local
RUN poetry install

COPY megano .

CMD [ "gunicorn", "--chdir", "megano_backend", "--bind", "0.0.0.0:8000", "diplomasite.wsgi:application" ]