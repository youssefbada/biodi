FROM nexus.retd.edf.fr/node:24.0.2-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci \
    --registry="https://nexus.retd.edf.fr/repository/mainnpm/" \
    --strict-ssl=false \
    --loglevel verbose

COPY . .

RUN npm run build -- --configuration production

# -------- Serve with Nginx --------
FROM nexus.retd.edf.fr/nginx:latest

# Angular build output
COPY --from=build /app/dist/biodiv-front/browser/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
