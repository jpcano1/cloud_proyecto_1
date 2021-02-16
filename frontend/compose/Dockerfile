FROM node:14

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD package.json $APP_DIR
ADD src $APP_DIR/src
ADD public $APP_DIR/public

ADD compose/start $APP_DIR
RUN sed -i 's/\r//' $APP_DIR/start
RUN chmod +x $APP_DIR/start

RUN apt-get update && apt full-upgrade -y && \
        apt-get install -y --no-install-recommends \
        tzdata \
        git \
        ffmpeg \
        vim \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN npm install
