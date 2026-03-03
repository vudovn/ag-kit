FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FIX: Forçar versões compatíveis com supabase_auth
RUN pip install --no-cache-dir --force-reinstall httpx==0.24.1 httpcore==0.17.3

# Copy app
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
