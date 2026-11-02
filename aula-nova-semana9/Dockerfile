FROM node:24-bookworm-slim
WORKDIR /usr/src/app
ENV NODE_ENV=production PORT=3000
COPY --chown=node:node package.json ./
COPY --chown=node:node app/ ./app/
COPY --chown=node:node backend/ ./backend/
USER node
EXPOSE 3000
CMD ["node", "backend/server.js"]