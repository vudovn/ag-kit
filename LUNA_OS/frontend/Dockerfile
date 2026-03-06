# Desenvolvimento rápido com cache otimizado
FROM node:20-alpine

WORKDIR /app

# Instalar dependências apenas se package files mudarem
COPY package.json package-lock.json* ./
RUN npm ci --prefer-offline --no-audit

# Copiar resto do código
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
