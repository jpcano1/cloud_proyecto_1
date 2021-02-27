FROM node:12.21.0 AS build

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD package.json $APP_DIR
ADD src $APP_DIR/src
ADD public $APP_DIR/public

RUN apt-get update && apt full-upgrade -y && \
        apt-get install -y --no-install-recommends \
        git \
        vim \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN npm install --silent

RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx","-g","daemon off;"]