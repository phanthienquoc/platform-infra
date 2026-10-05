FROM node:22-alpine
WORKDIR /app

COPY platform/auth-service/package.json ./package.json
RUN npm install --omit=dev

COPY platform/auth-service/src ./src
ENV NODE_ENV=production
EXPOSE 3000
CMD ["node", "src/server.mjs"]