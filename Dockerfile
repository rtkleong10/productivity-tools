ARG PYTHON_VERSION=3.10.0-slim-buster
FROM python:${PYTHON_VERSION}
ENV LANG C.UTF-8

RUN apt-get -y update && apt-get -y autoremove && apt-get -y install libpq-dev gcc

RUN mkdir -p /app
WORKDIR /app

RUN apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput


EXPOSE 8080

# replace APP_NAME with module name
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--access-logfile", "-", "productivity_tools.wsgi"]