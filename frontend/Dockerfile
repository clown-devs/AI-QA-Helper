FROM node:18-alpine AS build

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine AS production
COPY --from=build /frontend/dist /usr/share/nginx/html

COPY ./fullchain.pem /etc/ssl/certs/fullchain.pem 
COPY ./privkey.pem /etc/ssl/private/privkey.pem

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
