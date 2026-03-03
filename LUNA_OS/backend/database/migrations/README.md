# 🌙 LUNA OS - Migrações de Banco de Dados (Supabase)

Esta pasta contém as migrações SQL oficiais do projeto, organizadas na ordem exata de execução para garantir a integridade dos dados e o funcionamento das inteligências.

### 🚀 Ordem de Execução

Siga esta ordem rigorosamente ao configurar um novo ambiente ou atualizar o atual:

1.  **[01_infra_evolution.sql](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/database/migrations/01_infra_evolution.sql)**
    *   *O que faz:* Cria as tabelas base de inteligência, Dojo, health checks e **garante a unicidade da tabela `knowledge_base`** (necessário para o Seed funcionar sem erros).
    *   *Nota:* Inclui limpeza automática de duplicatas antes de aplicar a restrição UNIQUE.
    *   *Quando rodar:* Sempre primeiro.

2.  **[02_seed_haven_core.sql](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/database/migrations/02_seed_haven_core.sql)**
    *   *O que faz:* Alimenta o banco com a "Verdade dos Dados" da Haven (Serviços, Profissionais, Cupons, FAQs e infos de negócio).
    *   *Diferencial:* Usa `ON CONFLICT`, então você pode rodar várias vezes para atualizar os preços sem gerar erros.

3.  **[03_marketing_and_upsell.sql](file:///Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend/database/migrations/03_marketing_and_upsell.sql)**
    *   *O que faz:* Adiciona os recursos de campanhas de marketing e a lógica de Upsell para a LUNA oferecer serviços complementares.
    *   *Nota:* Inclui correções para evitar erros de "Relação já existe".

---
**Dica Soberana:** Sempre copie o conteúdo do arquivo e cole no [SQL Editor do Supabase](https://supabase.com/dashboard/project/sktrmwogifeuzrcnpvsw/sql/new).
