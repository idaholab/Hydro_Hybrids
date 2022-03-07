FROM node:lts-alpine as build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

WORKDIR /etc/nginx/conf.d
RUN rm default.conf
COPY nginx.conf .

CMD ["nginx", "-g", "daemon off;"]
