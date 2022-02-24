FROM node:14.4.0-alpine3.10 as build

WORKDIR /usr/src/app

COPY package.json /usr/src/app/package.json

RUN npm install
RUN npm install -g @vue/cli

COPY . /usr/src/app/
RUN npm run build

FROM node:lts-alpine

WORKDIR /app
RUN npm install -g http-server
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=build /usr/src/app/dist /app/dist

EXPOSE 8080