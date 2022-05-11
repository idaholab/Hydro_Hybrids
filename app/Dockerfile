FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN apk update && apk upgrade --available && sync

RUN npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:latest as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

WORKDIR /etc/nginx/conf.d
RUN rm default.conf
COPY nginx.conf .

CMD ["nginx", "-g", "daemon off;"]
