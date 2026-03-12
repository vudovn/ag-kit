# Project Charter — LUNA OS (Sovereign Management)

## Leis (P0 - Inquebráveis)
1. **Atendimento Humano em Primeiro Lugar**: A IA nunca deve fingir ser humana, mas deve ser tão eficiente quanto.
2. **Integridade do Banco**: Todas as queries ao Supabase devem respeitar o RLS (Row Level Security).
3. **Fluxo de Atendimento**: Nunca quebre o loop principal de recepção (`receptionist-flow`) ao adicionar novos agentes.
4. **Resgate de Contexto**: Cada nova mensagem deve recuperar o histórico do cliente antes de responder.

## Stack
- **Backend**: Python (FastAPI/Scripts).
- **Database**: Supabase (PostgreSQL).
- **Integration**: Evolution API (WhatsApp).
- **Workflow Engine**: Windmill.
- **AI**: Claude 3.5 Sonnet / Gemini Pro via OpenRouter.

## Objetivo
Transformar o atendimento da Escovaria Haven e do SORA Spa em uma experiência fluida, automatizada e lucrativa, gerenciando agendamentos, campanhas e dúvidas técnicas.

## Skills Base Ativas
- @evolution-skill
- @supabase-skill
- @prompt-skill
- @mct-brain-bridge
