---
name: hostinger-deploy
description: Configura deploy automático para Hostinger via FTP. Usa quando o usuário quer fazer deploy, publicar site, enviar arquivos para Hostinger, ou configurar FTP deploy.
---

# Hostinger Deploy via FTP

Esta skill configura o deploy automático de aplicações web para a Hostinger usando FTP.

## Quando Usar Esta Skill

- Usuário quer fazer deploy na Hostinger
- Usuário menciona "deploy", "publicar", "FTP", "Hostinger"
- Usuário quer configurar envio automático de arquivos
- Usuário quer criar comando `npm run deploy`

## Como Usar

### Passo 1: Verificar/Criar Arquivo .env

Primeiro, verifique se existe um arquivo `.env` no projeto:

**Se NÃO existir:** Crie o arquivo `.env` com o seguinte conteúdo:

```env
# ================================
# HOSTINGER FTP DEPLOY
# ================================
FTP_HOST=
FTP_USER=
FTP_PASSWORD=
FTP_REMOTE_PATH=/
```

**Se JÁ existir:** Adicione a seção de deploy ao final do arquivo:

```env

# ================================
# HOSTINGER FTP DEPLOY
# ================================
FTP_HOST=
FTP_USER=
FTP_PASSWORD=
FTP_REMOTE_PATH=/
```

### Passo 2: Solicitar Credenciais FTP ao Usuário

Pergunte ao usuário sobre as credenciais FTP com esta orientação:

---

**📋 Preciso das suas credenciais FTP da Hostinger para configurar o deploy.**

Para encontrar essas informações:

1. Acesse o painel da Hostinger (hpanel.hostinger.com)
2. Vá em **Arquivos** → **Contas FTP**
3. Crie uma conta FTP ou use uma existente

**Preencha as seguintes informações:**

| Campo | Onde encontrar | Exemplo |
|-------|----------------|---------|
| `FTP_HOST` | Aparece como "Hostname" na lista de contas FTP | `ftp.seudominio.com` ou IP do servidor |
| `FTP_USER` | Nome de usuário da conta FTP | `u123456789.ftp1` |
| `FTP_PASSWORD` | Senha definida ao criar a conta FTP | Sua senha |

**📁 Em qual pasta você quer fazer o deploy?**

- **Pasta raiz (`/`)** - Arquivos vão direto para a raiz do servidor (padrão)
- **Subpasta (ex: `/blog`, `/app`)** - Arquivos vão para uma subpasta específica

> Se não especificar, usarei `/` como padrão.

> **⚠️ IMPORTANTE:** Nunca compartilhe essas credenciais. O arquivo `.env` já está no `.gitignore`?

---

### Passo 3: Verificar .gitignore

Certifique-se de que `.env` está no `.gitignore`:

```
# Se não existir no .gitignore, adicione esta linha:
.env
```

### Passo 4: Instalar Dependência FTP

Execute o comando para instalar a biblioteca FTP:

```bash
npm install --save-dev basic-ftp
```

### Passo 5: Criar Script de Deploy

Crie o arquivo `scripts/deploy.js` na raiz do projeto:

```javascript
#!/usr/bin/env node

/**
 * Script de Deploy para Hostinger via FTP
 * Uso: npm run deploy
 */

const ftp = require('basic-ftp');
const path = require('path');
const fs = require('fs');

// Carrega variáveis de ambiente
require('dotenv').config();

const { FTP_HOST, FTP_USER, FTP_PASSWORD, FTP_REMOTE_PATH } = process.env;

// Detecta a pasta de build automaticamente
function detectBuildFolder() {
  const possibleFolders = ['dist', 'build', 'out', '.next', 'public'];
  for (const folder of possibleFolders) {
    if (fs.existsSync(folder)) {
      return folder;
    }
  }
  console.error('❌ Nenhuma pasta de build encontrada (dist, build, out, .next, public)');
  console.error('   Execute o build primeiro: npm run build');
  process.exit(1);
}

async function deploy() {
  // Valida credenciais
  if (!FTP_HOST || !FTP_USER || !FTP_PASSWORD) {
    console.error('❌ Credenciais FTP não configuradas!');
    console.error('   Configure as variáveis no arquivo .env:');
    console.error('   - FTP_HOST');
    console.error('   - FTP_USER');
    console.error('   - FTP_PASSWORD');
    process.exit(1);
  }

  const buildFolder = detectBuildFolder();
  const remotePath = FTP_REMOTE_PATH || '/';

  console.log('🚀 Iniciando deploy para Hostinger...');
  console.log(`   Host: ${FTP_HOST}`);
  console.log(`   Usuário: ${FTP_USER}`);
  console.log(`   Pasta local: ${buildFolder}`);
  console.log(`   Pasta remota: ${remotePath}`);
  console.log('');

  const client = new ftp.Client();
  client.ftp.verbose = false;

  try {
    console.log('🔌 Conectando ao servidor FTP...');
    await client.access({
      host: FTP_HOST,
      user: FTP_USER,
      password: FTP_PASSWORD,
      secure: false
    });
    console.log('✅ Conectado!');

    console.log(`📁 Navegando para ${remotePath}...`);
    await client.ensureDir(remotePath);

    console.log('📤 Enviando arquivos...');
    await client.uploadFromDir(buildFolder);

    console.log('');
    console.log('🎉 Deploy concluído com sucesso!');
    console.log(`   Seu site está disponível em: https://seudominio.com`);

  } catch (err) {
    console.error('');
    console.error('❌ Erro durante o deploy:');
    console.error(`   ${err.message}`);
    
    if (err.message.includes('Login incorrect')) {
      console.error('');
      console.error('💡 Dica: Verifique suas credenciais FTP no painel da Hostinger');
    }
    
    process.exit(1);
  } finally {
    client.close();
  }
}

deploy();
```

### Passo 6: Configurar package.json

Adicione o script de deploy no `package.json`:

```json
{
  "scripts": {
    "deploy": "npm run build && node scripts/deploy.js"
  }
}
```

> **Nota:** Se o projeto não tiver script de build, use apenas:
> ```json
> "deploy": "node scripts/deploy.js"
> ```

### Passo 7: Instalar dotenv (se necessário)

Se o projeto não tiver dotenv instalado:

```bash
npm install dotenv
```

## Árvore de Decisão

1. O projeto já tem `.env`?
   - Sim → Adicione a seção de FTP ao final
   - Não → Crie o arquivo completo

2. O projeto tem `package.json`?
   - Sim → Continue com instalação de dependências
   - Não → Crie um `package.json` primeiro com `npm init -y`

3. O projeto usa TypeScript/Build?
   - Sim → Use `"deploy": "npm run build && node scripts/deploy.js"`
   - Não → Use `"deploy": "node scripts/deploy.js"`

## Uso Final

Após configuração, o usuário pode fazer deploy com:

```bash
npm run deploy
```

O script irá:
1. ✅ Executar o build (se configurado)
2. ✅ Conectar ao servidor FTP da Hostinger
3. ✅ Enviar todos os arquivos da pasta de build
4. ✅ Mostrar mensagem de sucesso

## Troubleshooting

| Erro | Solução |
|------|---------|
| "Login incorrect" | Verifique usuário e senha no painel da Hostinger |
| "Connection refused" | Verifique se o host FTP está correto |
| "Nenhuma pasta de build" | Execute `npm run build` antes ou crie a pasta |
| "ETIMEDOUT" | Verifique sua conexão de internet |
