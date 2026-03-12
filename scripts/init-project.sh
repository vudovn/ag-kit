#!/bin/bash
# 🏗️ init-project.sh - Cria projeto com estrutura Antigravity Core v2.0

NAME=$1
if [ -z "$NAME" ]; then
    echo "❌ Erro: Informe o nome do projeto."
    exit 1
fi

PROJECT_DIR="/Users/franciscotaveira.ads/Documents/antigravity-kit/projects/$NAME"

if [ -d "$PROJECT_DIR" ]; then
    echo "❌ Erro: O projeto '$NAME' já existe."
    exit 1
fi

echo "🏗️  Iniciando Projeto Antigravity Core: $NAME..."

mkdir -p "$PROJECT_DIR"/{docs,src,.agent/skills}

# 1. PROJECT_CHARTER.md (A Constituição do Projeto)
cat > "$PROJECT_DIR/PROJECT_CHARTER.md" <<EOF
# Project Charter — $NAME

> [!NOTE]
> Este arquivo define a "Constituição" do projeto. Edite as regras abaixo para alinhar todas as IAs.

## 🛡️ Segurança (P0)
- **Autenticação**: [Ex: JWT via Supabase Auth]
- **Políticas RLS**: [Ex: Todas as tabelas devem ter RLS ativo]
- **API Keys**: Nunca expor \`service_role\` no frontend.

## 🏗️ Backend & Logística
- **Padronização**: [Ex: Funções modulares, tratamento de erro global]
- **Integrações**: [Ex: Evolution API v1.x, Windmill para jobs]

## 🎨 Frontend & UX
- **Design System**: [Ex: Vanilla CSS + Glassmorphism]
- **Componentes**: [Ex: Reutilizáveis, foco em acessibilidade]

## 📊 Dados & Verdade
- **Filosofia**: Truth in Data (Dados reais ou estado vazio, nunca mocks)
- **Schema**: PostgreSQL via Supabase.

## 📖 Documentação & Padrões
- **Comentários**: [Ex: Padrão JSDoc ou Python type hints]
- **Codebase Map**: Este projeto deve manter o \`CODEBASE.md\` atualizado a cada grande mudança.

## 🎯 Objetivo & Contexto
[Descreva o que o projeto resolve e quem é o usuário final]

## 🧠 Brain Skills
- @mct-brain-bridge
EOF

# 2. CODEBASE.md (O Mapa da Mina)
cat > "$PROJECT_DIR/CODEBASE.md" <<EOF
# Codebase Map — $NAME

## Estado Atual
- Projeto inicializado.

## Pontos de Entrada
- Charter: PROJECT_CHARTER.md
- Docs: docs/
- Source: src/
EOF

# 3. Executar Sync Inicial
/Users/franciscotaveira.ads/Documents/antigravity-kit/scripts/sync-context.sh "$NAME"

echo ""
echo "✅ Projeto '$NAME' criado com sucesso!"
echo "📍 Local: $PROJECT_DIR"
echo "🌟 Para IA, use: projects/\$NAME/MCT-MASTER-DIRECTIVE.md"
