FROM node:12.21.0 AS build

ENV APP_DIR /app
WORKDIR $APP_DIR

ADD package.json $APP_DIR
ADD src $APP_DIR/src
ADD public $APP_DIR/public

RUN npm install --silent

ENV REACT_APP_API_URL http://0.0.0.0:
ENV REACT_APP_PORT 80

RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=build /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx","-g","daemon off;"]