FROM node:12.21.0 AS build

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD package.json $APP_DIR
ADD src $APP_DIR/src
ADD public $APP_DIR/public

RUN npm install --silent

ENV REACT_APP_API_URL ${REACT_APP_API_URL}
ENV REACT_APP_PORT ${REACT_APP_PORT}

RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx","-g","daemon off;"]