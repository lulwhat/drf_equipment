FROM node:20-alpine

RUN apk add --no-cache openssl

WORKDIR /app

COPY ./equipment-frontend/package*.json ./

RUN npm install

COPY ./equipment-frontend/ .

RUN npm run build

# Only for debug
# CMD ["npm", "run", "preview"]