FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
# Normally we'd use nginx to serve the dist folder in production, but for scaffolding we can use vite preview
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
