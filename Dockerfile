FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y \
  build-essential \
  tzdata \
  libpq-dev \
  postgresql-client \
  subversion \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY requirements-dev.txt /app/requirements-dev.txt
ARG installdev=false
RUN if [ "${installdev}" = "true" ] ; \
      then pip install --no-cache-dir -r /app/requirements-dev.txt ; \
    fi

ADD . /app

ENV PYTHONPATH /app
CMD ["python", "run_server.py"]
