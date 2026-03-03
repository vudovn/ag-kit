# 🩺 LUNA OS — Debugging & Troubleshooting Log

Este arquivo documenta erros críticos encontrados durante o desenvolvimento e os padrões de correção aplicados para evitar regressões.

---

## 🛑 Armadilha: Trailing Slash (Barra Final)

### Problema
O Next.js (frontend) e o FastAPI (backend) divergem sobre como lidar com a barra final nas URLs (ex: `/api/conversations/` vs `/api/conversations`).

1. **Next.js Proxy:** Por padrão, redireciona rotas com barra para sem barra (308 Permanent Redirect).
2. **FastAPI Context:** Com `redirect_slashes=False`, ele trata as duas como rotas diferentes. Chamadas vindas do frontend com barra resultavam em 404 ou falha de CORS devido ao redirect automático do Next.js.

### ✅ Correção (Padrão LUNA)
1. **Frontend:** Sempre chamar endpoints **sem** barra final.
   - ❌ `fetch('/api/clients/')`
   - ✅ `fetch('/api/clients')`
2. **Backend Routers:** Usar decorator duplo para suportar ambos os casos e evitar 404 inesperados.
   ```python
   @router.get("")   # Sem barra
   @router.get("/")  # Com barra
   async def list_items(): ...
   ```
3. **Next Config:** Forçar `trailingSlash: false` no `next.config.js`.

---

## 🗺️ Mapeamento de Dados (Flattening)

### Problema
A API do backend retornava objetos aninhados (seguindo o padrão Supabase), mas a UI do frontend esperava campos diretos no primeiro nível para facilitar a filtragem e exibição.

- **API Original:** `{ "id": 1, "client": { "name": "Ana", "phone": "..." } }`
- **UI Esperava:** `{ "id": 1, "client_name": "Ana", "client_phone": "..." }`

### ✅ Correção
Implementação da função helper `normalize_conv` no backend para achatar o objeto antes de retornar ao frontend.
```python
def normalize_conv(c: dict) -> dict:
    client = c.pop("client", None) or {}
    c["client_name"] = client.get("name") or c.get("phone", "")
    c["client_phone"] = client.get("phone") or c.get("phone", "")
    return c
```

---

## 🔗 Roteamento Genérico vs Específico

### Problema
Rotas com IDs dinâmicos (ex: `/{conversation_id}`) capturavam rotas específicas (ex: `/active` ou `/handoffs`) se fossem declaradas antes delas.

### ✅ Correção
Sempre declarar rotas estáticas/específicas **antes** das rotas dinâmicas com parâmetros.

---

## 🌐 Configuração de Proxy (Next.js)

Para que o frontend consiga conversar com o backend dentro da rede Docker, o `next.config.js` deve usar o nome do serviço definido no `docker-compose.yml`.

**Padrão Seguro:**
```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*/', // Com barra
      destination: 'http://luna-backend:8000/api/:path*',
    },
    {
      source: '/api/:path*',  // Sem barra
      destination: 'http://luna-backend:8000/api/:path*',
    },
  ]
}
```

---
*MCT OS — Poder invisível, simplicidade visível.*
