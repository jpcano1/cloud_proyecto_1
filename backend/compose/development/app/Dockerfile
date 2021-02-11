FROM python:3.8-slim

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD src $APP_DIR/src
ADD requirements/dev.txt $APP_DIR
ADD wsgi.py $APP_DIR

# Run Commands
ADD compose/development/app/start $APP_DIR
RUN sed -i 's/\r//' $APP_DIR/start
RUN chmod +x $APP_DIR/start

ADD compose/development/celery/worker/start $APP_DIR/celery_worker_start
RUN sed -i 's/\r//' $APP_DIR/celery_worker_start
RUN chmod +x $APP_DIR/celery_worker_start

ADD compose/development/celery/beat/start $APP_DIR/celery_beat_start
RUN sed -i 's/\r//' $APP_DIR/celery_beat_start
RUN chmod +x $APP_DIR/celery_beat_start

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        apt-utils \
        git \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install -r dev.txt