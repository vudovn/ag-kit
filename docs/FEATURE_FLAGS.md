# 🚩 Feature Flags Configuration

## Configuração Central de Feature Flags

---

## 📋 Feature Flags Ativos

| Feature | Flag | Default | Status |
|---------|------|---------|--------|
| **Smart Caching** | `FEATURE_SMART_CACHE` | `true` | ✅ Production |
| **Human Handoff** | `FEATURE_HANDOFF` | `true` | ✅ Production |
| **Dual Mode MCP** | `FEATURE_DUAL_MODE_MCP` | `true` | ✅ Production |
| **Multi-Brain V2** | `FEATURE_MULTI_BRAIN_V2` | `false` | 🧪 Staging |
| **Memory Chain** | `FEATURE_MEMORY_CHAIN` | `false` | 🚧 Development |
| **Behavioral DNA** | `FEATURE_BEHAVIORAL_DNA` | `false` | 🚧 Development |

---

## 🔧 Configuração (.env)

```bash
# .env file

# ============================================
# FEATURE FLAGS - LUNA Multi-Brain V2
# ============================================

# Smart Caching (Production Ready)
# Reduz API calls em 100x
FEATURE_SMART_CACHE=true
SMART_CACHE_TTL=300          # 5 minutes
SMART_CACHE_MAX_SIZE=1000    # 1000 contacts

# Human Handoff (Production Ready)
# Handoff inteligente para humanos
FEATURE_HANDOFF=true
HANDOFF_CONFIDENCE_THRESHOLD=0.5
HANDOFF_MAX_AI_FAILURES=2
HANDOFF_VIP_LTV_THRESHOLD=10000

# Dual Mode MCP (Production Ready)
# stdio + HTTP modes
FEATURE_DUAL_MODE_MCP=true
DUAL_MODE_DEFAULT=stdio      # stdio ou http
HTTP_MODE_PORT=3000
HTTP_MODE_HOST=0.0.0.0

# Multi-Brain V2 (Staging)
# Roteamento inteligente de cérebros
FEATURE_MULTI_BRAIN_V2=false
MULTI_BRAIN_QUICK=haiku      # Rotinas simples
MULTI_BRAIN_STANDARD=sonnet  # Chat normal
MULTI_BRAIN_COMPLEX=opus     # Casos sensíveis

# Memory Chain (Development)
# Audit trail SHA-256
FEATURE_MEMORY_CHAIN=false
MEMORY_CHAIN_ALGORITHM=sha256

# Behavioral DNA (Development)
# Personalização por cliente
FEATURE_BEHAVIORAL_DNA=false
BEHAVIORAL_DNA_DEFAULT_TONE=professional

# ============================================
# MONITORING
# ============================================
LOG_LEVEL=INFO
SENTRY_DSN=
METRICS_ENABLED=true
```

---

## 📖 Uso em Código

### Verificar Feature Flag

```python
# brain/features.py
import os

def is_feature_enabled(feature_name: str, default: bool = False) -> bool:
    """Check if feature is enabled"""
    env_var = f"FEATURE_{feature_name.upper()}"
    return os.getenv(env_var, str(default)).lower() == "true"

# Usage
if is_feature_enabled("smart_cache"):
    # Use smart caching
    contact = contact_cache.get(contact_id)
else:
    # Fallback to direct CRM
    contact = crm.get_contact(contact_id)
```

### Feature Decorator

```python
# brain/features.py
from functools import wraps

def feature_required(feature_name: str):
    """Decorator to require feature flag"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_feature_enabled(feature_name):
                raise FeatureDisabledError(f"Feature {feature_name} is disabled")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@feature_required("smart_cache")
def get_cached_contact(contact_id: str):
    """Get contact with caching (only if feature enabled)"""
    return contact_cache.get(contact_id)
```

---

## 🔄 Rollback Procedure

### Rollback Rápido (Segundos)

```bash
# 1. Desabilitar feature
export FEATURE_SMART_CACHE=false

# 2. Restart service
systemctl restart luna-brain

# 3. Verify
curl http://localhost:3000/health
```

### Rollback Automático

```python
# brain/monitoring/auto_rollback.py
import os
import sentry_sdk

ERROR_THRESHOLD = 0.01  # 1%

def check_and_rollback():
    """Automatic rollback if error rate > threshold"""
    error_rate = sentry_sdk.get_error_rate()
    
    if error_rate > ERROR_THRESHOLD:
        # Rollback all features
        features_to_disable = [
            "SMART_CACHE",
            "HANDOFF",
            "DUAL_MODE_MCP",
            "MULTI_BRAIN_V2"
        ]
        
        for feature in features_to_disable:
            os.system(f"echo 'FEATURE_{feature}=false' >> .env.rollback")
        
        # Restart service
        os.system("systemctl restart luna-brain")
        
        # Send alert
        send_alert(f"Automatic rollback executed! Error rate: {error_rate:.2%}")
```

---

## 📊 Monitoring Dashboard

### Feature Flag Stats

```python
# brain/monitoring/feature_stats.py
from brain.cache import contact_cache
from brain.handoff import handoff_engine

def get_feature_stats():
    """Get statistics for all features"""
    return {
        "smart_cache": contact_cache.get_stats(),
        "human_handoff": handoff_engine.get_stats(),
        "feature_flags": {
            "smart_cache": is_feature_enabled("smart_cache"),
            "handoff": is_feature_enabled("handoff"),
            "dual_mode_mcp": is_feature_enabled("dual_mode_mcp"),
            "multi_brain_v2": is_feature_enabled("multi_brain_v2")
        }
    }

# Output
{
  "smart_cache": {
    "hit_rate": "95.23%",
    "entries": 234,
    "memory_mb": 2.34
  },
  "human_handoff": {
    "pending": 3,
    "resolved": 15,
    "avg_time_to_accept": 12.5
  },
  "feature_flags": {
    "smart_cache": true,
    "handoff": true,
    "dual_mode_mcp": true,
    "multi_brain_v2": false
  }
}
```

---

## 🧪 Staging vs Production

### Staging (.env.staging)

```bash
# All features enabled for testing
FEATURE_SMART_CACHE=true
FEATURE_HANDOFF=true
FEATURE_DUAL_MODE_MCP=true
FEATURE_MULTI_BRAIN_V2=true      # Test new version
FEATURE_MEMORY_CHAIN=true        # Test new feature
FEATURE_BEHAVIORAL_DNA=true      # Test new feature
```

### Production (.env.production)

```bash
# Only stable features
FEATURE_SMART_CACHE=true
FEATURE_HANDOFF=true
FEATURE_DUAL_MODE_MCP=true
FEATURE_MULTI_BRAIN_V2=false     # Not yet
FEATURE_MEMORY_CHAIN=false       # Not yet
FEATURE_BEHAVIORAL_DNA=false     # Not yet
```

---

## 🚀 Deploy com Feature Flags

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy with Feature Flags

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set environment
        run: |
          if [ ${{ github.ref }} == 'refs/heads/main' ]; then
            echo "ENV=production" >> $GITHUB_ENV
            cp .env.production .env
          else
            echo "ENV=staging" >> $GITHUB_ENV
            cp .env.staging .env
          fi
      
      - name: Run tests
        run: pytest tests/ -v
      
      - name: Deploy
        run: |
          ./scripts/deploy.sh
          echo "Deployed to ${{ env.ENV }}"
          echo "Feature flags:"
          grep "^FEATURE_" .env
```

---

## 📈 Feature Adoption Metrics

### Track Feature Usage

```python
# brain/analytics/feature_usage.py
from datetime import datetime, timedelta

class FeatureUsageTracker:
    def __init__(self):
        self.usage = {}
    
    def track(self, feature: str, user_id: str, success: bool):
        """Track feature usage"""
        key = f"{feature}:{datetime.now().date()}"
        
        if key not in self.usage:
            self.usage[key] = {"total": 0, "success": 0, "users": set()}
        
        self.usage[key]["total"] += 1
        if success:
            self.usage[key]["success"] += 1
        self.usage[key]["users"].add(user_id)
    
    def get_daily_stats(self, feature: str, days: int = 7):
        """Get daily usage stats for feature"""
        stats = []
        for i in range(days):
            date = datetime.now().date() - timedelta(days=i)
            key = f"{feature}:{date}"
            
            if key in self.usage:
                data = self.usage[key]
                stats.append({
                    "date": str(date),
                    "total": data["total"],
                    "success_rate": data["success"] / data["total"] * 100,
                    "unique_users": len(data["users"])
                })
        
        return stats

# Usage
tracker = FeatureUsageTracker()
tracker.track("smart_cache", "user_123", success=True)
stats = tracker.get_daily_stats("smart_cache")
```

---

## ✅ Feature Flag Checklist

### Antes de Habilitar

- [ ] Testes passando (100%)
- [ ] Code review aprovado
- [ ] Staging testado (24h+)
- [ ] Rollback plan documentado
- [ ] Monitoring configurado
- [ ] Alertas configurados
- [ ] Docs atualizadas

### Depois de Habilitar

- [ ] Monitorar erro rate (< 1%)
- [ ] Monitorar latência (sem degradação)
- [ ] Monitorar adoção (> 80% em 7 dias)
- [ ] Coletar feedback (usuários)
- [ ] Documentar learnings

---

## 🔗 Links Relacionados

- `brain/cache.py` - Smart Caching
- `brain/handoff.py` - Human Handoff
- `docs/SMART_CACHING.md` - Smart Caching Guide
- `docs/HUMAN_HANDOFF.md` - Handoff Guide
- `docs/IMPLEMENTATION_PACT.md` - Implementation Pact

---

**Versão:** 1.0.0  
**Status:** ✅ Production Ready  
**Última Atualização:** 2026-03-12
