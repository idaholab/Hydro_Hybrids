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
RUN apk upgrade --update-cache --available 
RUN apk add openssl 
RUN openssl req -x509 -nodes -days 365000 -subj "/CN=hydrohybrids.azure.inl.gov" -addext "subjectAltName=DNS:hydrohybrids.azure.inl.gov" -newkey rsa:2048 -keyout /etc/nginx/nginx-selfsigned.key -out /etc/nginx/nginx-selfsigned.crt
CMD ["nginx", "-g", "daemon off;"]
