FROM node:lts-alpine as build-stage

WORKDIR /usr/src/app

COPY . .

# RUN npm config set cafile "/usr/src/app/certs/CAINLROOT.crt"
RUN npm install

RUN npm run build

# production stage
FROM nginx:latest as production-stage

COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html

RUN apt-get update && apt-get -y upgrade

WORKDIR /etc/nginx/conf.d
RUN rm default.conf
COPY nginx.conf .

CMD ["nginx", "-g", "daemon off;"]
