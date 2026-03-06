FROM python:3.11-slim

WORKDIR /app

# Instalar dependências com cache
COPY requirements.txt .

# Instalar apenas o necessário (sem cache pip para build menor)
RUN pip install --no-cache-dir -r requirements.txt

# FIX: Forçar versões compatíveis com supabase_auth
RUN pip install --no-cache-dir --force-reinstall httpx==0.24.1 httpcore==0.17.3

# Copiar app (apenas após install para melhor cache)
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
