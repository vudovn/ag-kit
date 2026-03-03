# Dockerfile para Kimi-Dev Soberano
FROM python:3.12-slim

# Instalar dependências de sistema essenciais
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    curl \
    make \
    build-essential \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Inicializar git-lfs
RUN git lfs install

# Instalar 'uv' para gerenciamento de pacotes
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Definir diretório de trabalho
WORKDIR /app

# Clonar Kimi-Dev oficialmente (ou copiar se houver fonte local)
RUN git clone https://github.com/MoonshotAI/Kimi-Dev.git .

# Instalar dependências do projeto via uv
RUN uv pip install --system -e .

# Expor portas se necessário (ex: para vLLM local futuramente)
EXPOSE 8000

# Script de entrada para download de dados se necessário
COPY scripts/bootstrap.sh /usr/local/bin/bootstrap.sh
RUN chmod +x /usr/local/bin/bootstrap.sh

ENTRYPOINT ["/usr/local/bin/bootstrap.sh"]
