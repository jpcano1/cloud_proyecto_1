FROM python:3.8

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD src $APP_DIR/src
ADD requirements.txt $APP_DIR
ADD wsgi.py $APP_DIR

# Run Commands
ADD compose/production/app/start $APP_DIR
RUN sed -i 's/\r//' $APP_DIR/start
RUN chmod +x $APP_DIR/start

ADD compose/production/celery/worker/start $APP_DIR/celery_worker_start
RUN sed -i 's/\r//' $APP_DIR/celery_worker_start
RUN chmod +x $APP_DIR/celery_worker_start

ADD compose/production/celery/beat/start $APP_DIR/celery_beat_start
RUN sed -i 's/\r//' $APP_DIR/celery_beat_start
RUN chmod +x $APP_DIR/celery_beat_start

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt full-upgrade -y && \
        apt-get install -y --no-install-recommends \
        tzdata \
        git \
        ffmpeg \
        vim \
        libcurl4-gnutls-dev \
        librtmp-dev \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip install -q --upgrade pip
RUN pip install -q -r requirements.txt
RUN pip install -q unittest2