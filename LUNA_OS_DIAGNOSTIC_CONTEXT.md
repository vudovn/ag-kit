# 🪐 LUNA OS v3.0 - Sovereign Diagnostic Context

**MCT Master AI Diagnostic Document**  
Este documento é o "State of the Union" da máquina **LUNA OS**. Ele serve como mapa mental para **qualquer outra Inteligência Artificial** realizar um diagnóstico preciso da nossa arquitetura, localização de arquivos e estado atual das integrações.

---

## 🏗️ 1. Arquitetura Geral & Stack

O **LUNA OS** é um ecossistema operacional de Atendimento, Vendas e Agendamento para Clínicas (atualmente rodando na licença *Haven*). A arquitetura é baseada nos princípios *Sovereign* da MCT (Truth in Data, Fail Fast, Zero Alucinações).

- **Backend:** `Python 3.10+ / FastAPI` (Motor Lógica & Integrações)
- **Frontend:** `Node.js / React / Next.js` (Painel Administrativo)
- **Gateway WhatsApp:** `Evolution API` via Docker (Portas 8080/8081)
- **LLM Router:** `OpenRouter`
- **Sovereign Database:** `Supabase` (PostgreSQL - Sessões, Clientes, Histórico)
- **Sovereign Memory:** `Obsidian` (Vault local de CRM e Knowledge Items)

**Localização Raiz do Projeto:**  
`/Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/`

---

## 🗺️ 2. Mapeamento de Diretórios Críticos

### 🖥️ A. Backend (`LUNA_OS/backend/`)
O coração da aplicação. Roda o Cérebro, Webhooks e Workers via `uvicorn`.

- **`app/main.py`**: Ponto de entrada (App FastAPI) e Registro de Rotas HTTP.
- **`app/config.py`**: Gerente de Variáveis de Ambiente e credenciais (`BELASIS_MOCK=True` está aqui).
- **`app/api/` (Endpoints)**
  - `webhooks.py`: Onde as mensagens do Evolution API batem e são processadas pro Brain.
  - `campaigns.py` / `analytics_super.py`: Regras de negócio do Dashboard e Campanhas.
  - `settings.py`: Controle das keys e configurações do dual-brain injetadas do frontend.
- **`app/core/` (Lógica Pura)**
  - `brain.py`: O "Cérebro". Usa a arquitetura **Dual Brain**: Faz Classificação de Intenções (regex + regex emulada), constrói System Prompts com histórico (RAG se existir) e decide ações.
  - `memory.py`: Faz a interface com o Supabase. Grava/Recupera `conversations` (o contexto ativo de uma sessão WhatsApp) e `extracted_data` (o que a LUNA descobre).
  - `scheduler.py`: A Máquina de Estado do Agendamento. Ele aciona o `BelasisClient` e diz à LUNA o que perguntar a seguir (Data, Hora, Profissional) até terminar a reserva.
- **`app/integrations/` (Camadas Externas)**
  - `belasis.py`: O Wrapper oficial do ERP da Clínica (agendamentos de verdade/mock).
  - `evolution.py`: Wrapper para mandar mensagens de volta pelo WhatsApp.
  - `openrouter.py`: Wrapper Genérico Universal para falar com as IAs (DeepSeek, Claude, Llama).
- **`app/scripts/`**
  - Scripts de simulação como `test_booking_flow.py` ou `auto_conversa_simulator.py` (Dojo Arena) que rodam testes assíncronos offline contra o Cérebro para evitar debugs custosos com a Evolution.

### 🧠 B. O Cérebro Contínuo (`LUNA_OS/backend/app/knowledge/obsidian_vault/`)
Uma inovação MCT. O Supabase é a memória *básica*, mas o Obsidian é o cérebro *profundo* do projeto. Nele, arquivos markdown reais são gerados para compilar os dados da clínica em tempo real.
- **`000_MCT_MASTER_INDEX.md`**: O Painel Principal que agrega Dataviews sobre os clientes.
- **`CRM/`**: Onde os históricos e dados ricos em formato ".md" são armazenados pelas IAs.
- **`copilot/copilot-custom-prompts/`**: Comandos criados pelo Francisco para facilitar o uso interno (ex: "MCT: Code Review", "LUNA: Auditor do Dojo").
- Tudo aqui está conectado num "Graph View" para a gestão clínica e auditorias locais.

### 🎨 C. Frontend Administrativo (`LUNA_OS/frontend/`)
- Portal React puro de manipulação das configurações.
- Conecta no Evolution (Iframe / Gerenciamento de QRCode).
- Páginas chaves: `app/brain/page.tsx` (Personalidade) e `app/settings/page.tsx` (Modelos e Chaves).

---

## ⚡ 3. O que foi feito recentemente (Últimas Iterações)?

Para contexto do diagnóstico da IA, aqui estão os últimos problemas resolvidos na versão 3.0:

1. **Implementação do Dual Brain (`brain.py`)**: Devido ao problema de "alucinação" grave. A `LunaBrain.process_message` foi dívida.
   - **Start**: DeepSeek-R1 (Lógico/Matemático) processa a Regra e extrai os campos no formato JSON Invisível limitando as possibilidades.
   - **Fim**: Claude-3.5-Sonnet (Voz/Carisma) lê a resposta da DeepSeek e transforma na mensagem calorosa para o WhatsApp.
2. **Integração Belasis**: Criação do `scheduler.py` e `belasis.py`. Fluxos de múltiplas etapas ("Agendar > Qual Serviço > Amanhã > 14h") estão blindados. O sistema consulta a API do Belasis para achar slots e responde com regras rígidas.
3. **Persistência Multi-Turno**: Havia um bug crítico em `memory.py` onde a "Conversa Ativa" não era criada em background. Resolvido; a etapa do Supabase salva `extracted_data` persistentemente nas conversas longas de Agendamento.
4. **Organização Obsidian Graph**: Arquivos huem de 300 logs de CRM não estavam lidos pelo Graph View. Um script varreu o Vault adicionando a "Tag: `#crm`" e links silenciosos para o Index central. Instalamos os "Copilot Custom Prompts".

---

## 🚨 4. Como Diagnosticar (Para a Outra IA)

Se o Francisco pedir a você para debugar ou planejar uma feature a partir deste mapa, considere o seguinte fluxo de resolução de problemas MCT:

*   **Problemas em Agendamentos/Integrações via WhatsApp?**
    *   Siga a trilha: `api/webhooks.py` → `core/brain.py` → `core/scheduler.py` → `integrations/belasis.py`. Verifique se o objeto `extracted_data` está chegando de `memory.get_extracted_data()`.
*   **Problemas de Frontend React / Supabase RLS?**
    *   Verifique se o token de serviço do `.env` na pasta principal do `LUNA_OS/` não expirou, e olhe as chamadas de banco partindo direta do `frontend/app`.
*   **Problemas Cognitivos da LUNA (Alucinações / Bug de Fluxo)?**
    *   Verifique a estrutura de `prompt` na função `build_logic_prompt()` e `build_voice_prompt()` dentro de `core/brain.py`. A lógica sempre dita a regra, a voz apenas colore.
*   **A "Memória não segura" informações?**
    *   Sempre valide o arquivo `memory.py`. Verifique as tabelas `clients` e `conversations` localizadas no schema do Supabase. Todo *state* local que a IA deve lembrar repousa lá.

> _Ao final do dia, se quebrar, verifique se a Variável de Ambiente `BELASIS_MOCK=True` está ativada. Grande parte dos fluxos hoje dependem de testes no Dojo usando MOCK._
