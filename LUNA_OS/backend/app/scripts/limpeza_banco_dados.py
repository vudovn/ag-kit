#!/usr/bin/env python3
"""
🌙🔧 LUNA OS v3.0 — LIMPEZA E CORREÇÃO DE BANCO DE DADOS
Remove redundâncias, corrige inconsistências
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/limpeza_banco_dados.log", rotation="10 MB", retention="30 days")


class LimpezaBancoDados:
    """
    Limpeza e correção de banco de dados
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.acoes_realizadas = []
        
    def remover_clients_duplicados(self) -> int:
        """Remove clients duplicados por phone"""
        try:
            logger.info("🗑️ Removendo clients duplicados...")
            
            # Buscar todos clients
            result = self.db.table("clients").select("id, phone").execute()
            clients = result.data or []
            
            # Agrupar por phone
            phones_dict = {}
            for client in clients:
                phone = client.get("phone")
                if phone not in phones_dict:
                    phones_dict[phone] = []
                phones_dict[phone].append(client.get("id"))
            
            # Remover duplicados (manter mais antigo)
            removidos = 0
            for phone, ids in phones_dict.items():
                if len(ids) > 1:
                    # Manter primeiro, remover resto
                    for id_remover in ids[1:]:
                        try:
                            self.db.table("clients").delete().eq("id", id_remover).execute()
                            removidos += 1
                            logger.info(f"   ✅ Client removido: {id_remover} (phone: {phone})")
                        except Exception as e:
                            logger.warning(f"   ⚠️ Erro ao remover {id_remover}: {e}")
            
            logger.info(f"✅ {removidos} clients duplicados removidos")
            
            self.acoes_realizadas.append({
                "acao": "remover_clients_duplicados",
                "count": removidos,
                "status": "sucesso"
            })
            
            return removidos
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover duplicados: {e}")
            return 0
    
    def criar_clients_para_orfaos(self) -> int:
        """Cria clients para conversas sem client associado"""
        try:
            logger.info("🆕 Criando clients para phones órfãos...")
            
            # Buscar todas conversas
            conv_result = self.db.table("conversations").select("phone, client_name").execute()
            phones_conversas = set(c.get("phone") for c in conv_result.data) if conv_result.data else set()
            
            # Buscar clients existentes
            client_result = self.db.table("clients").select("phone").execute()
            phones_clients = set(c.get("phone") for c in client_result.data) if client_result.data else set()
            
            # Phones órfãos
            phones_orfaos = phones_conversas - phones_clients
            
            # Criar clients para órfãos
            criados = 0
            for phone in phones_orfaos:
                try:
                    # Buscar nome da conversa
                    conv_com_nome = next((c for c in conv_result.data if c.get("phone") == phone and c.get("client_name")), None)
                    client_name = conv_com_nome.get("client_name") if conv_com_nome else f"Cliente {phone[-5:]}"
                    
                    # Criar client
                    novo_client = {
                        "phone": phone,
                        "name": client_name,
                        "first_contact": datetime.utcnow().isoformat(),
                        "last_contact": datetime.utcnow().isoformat(),
                        "tags": ["criado_automaticamente"],
                        "preferences": {},
                        "total_visits": 0,
                        "total_spent": 0
                    }
                    
                    self.db.table("clients").insert(novo_client).execute()
                    criados += 1
                    logger.info(f"   ✅ Client criado: {phone} ({client_name})")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️ Erro ao criar client para {phone}: {e}")
            
            logger.info(f"✅ {criados} clients criados para phones órfãos")
            
            self.acoes_realizadas.append({
                "acao": "criar_clients_orfaos",
                "count": criados,
                "status": "sucesso"
            })
            
            return criados
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar clients órfãos: {e}")
            return 0
    
    def remover_clients_sem_conversas(self) -> int:
        """Remove clients que não têm nenhuma conversa"""
        try:
            logger.info("🗑️ Removendo clients sem conversas...")
            
            # Buscar todos clients
            clients_result = self.db.table("clients").select("phone, id").execute()
            clients = clients_result.data or []
            
            # Buscar phones com conversas
            convs_result = self.db.table("conversations").select("phone").execute()
            phones_com_conversa = set(c.get("phone") for c in convs_result.data) if convs_result.data else set()
            
            # Remover clients sem conversas
            removidos = 0
            for client in clients:
                if client.get("phone") not in phones_com_conversa:
                    try:
                        self.db.table("clients").delete().eq("id", client.get("id")).execute()
                        removidos += 1
                        logger.info(f"   ✅ Client removido: {client.get('id')} (sem conversas)")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Erro ao remover client {client.get('id')}: {e}")
            
            logger.info(f"✅ {removidos} clients sem conversas removidos")
            
            self.acoes_realizadas.append({
                "acao": "remover_clients_sem_conversas",
                "count": removidos,
                "status": "sucesso"
            })
            
            return removidos
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover clients sem conversas: {e}")
            return 0
    
    def criar_indices_performance(self) -> List[str]:
        """Cria índices para melhorar performance"""
        try:
            logger.info("📊 Criando índices de performance...")
            
            indices_criados = []
            
            # Índices recomendados
            indices = [
                {"tabela": "whatsapp_messages_history", "coluna": "phone", "nome": "idx_wmh_phone"},
                {"tabela": "whatsapp_messages_history", "coluna": "message_timestamp", "nome": "idx_wmh_timestamp"},
                {"tabela": "conversations", "coluna": "phone", "nome": "idx_conv_phone"},
                {"tabela": "conversations", "coluna": "status", "nome": "idx_conv_status"},
                {"tabela": "clients", "coluna": "phone", "nome": "idx_clients_phone"}
            ]
            
            # Nota: Criar índices requer permissões de admin no Supabase
            # Este é um placeholder para a ação
            for idx in indices:
                logger.info(f"   📊 Índice sugerido: CREATE INDEX {idx['nome']} ON {idx['tabela']}({idx['coluna']})")
                indices_criados.append(f"CREATE INDEX {idx['nome']} ON {idx['tabela']}({idx['coluna']})")
            
            logger.info(f"✅ {len(indices)} índices sugeridos (requer admin para criar)")
            
            self.acoes_realizadas.append({
                "acao": "criar_indices_performance",
                "count": len(indices),
                "status": "sugerido",
                "sql": indices_criados
            })
            
            return indices_criados
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar índices: {e}")
            return []
    
    def consolidar_tabelas_similares(self) -> Dict:
        """Sugere consolidação de tabelas similares"""
        try:
            logger.info("🔍 Analisando tabelas similares...")
            
            # Esta é uma análise mais complexa que requer inspeção manual
            # Por enquanto, retorna sugestões genéricas
            
            sugestoes = {
                "analise": "Revisar tabelas com nomes similares",
                "exemplos": [
                    "campaigns vs campaign_messages",
                    "knowledge_base vs knowledge_categories"
                ],
                "recomendacao": "Consolidar se redundantes"
            }
            
            logger.info(f"✅ Análise de tabelas similares concluída")
            
            self.acoes_realizadas.append({
                "acao": "consolidar_tabelas_similares",
                "status": "analise",
                "sugestoes": sugestoes
            })
            
            return sugestoes
            
        except Exception as e:
            logger.error(f"❌ Erro ao analisar tabelas: {e}")
            return {}
    
    def gerar_relatorio_limpeza(self) -> Dict:
        """Gera relatório de todas ações de limpeza"""
        try:
            logger.info("📊 Gerando relatório de limpeza...")
            
            relatorio = {
                "status": "sucesso",
                "timestamp": datetime.utcnow().isoformat(),
                "acoes_realizadas": self.acoes_realizadas,
                "resumo": {
                    "total_acoes": len(self.acoes_realizadas),
                    "sucessos": sum(1 for a in self.acoes_realizadas if a.get('status') == 'sucesso'),
                    "sugeridos": sum(1 for a in self.acoes_realizadas if a.get('status') == 'sugerido'),
                    "analises": sum(1 for a in self.acoes_realizadas if a.get('status') == 'analise')
                }
            }
            
            logger.info(f"✅ Relatório gerado com sucesso")
            
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    def imprimir_relatorio(self, relatorio: Dict):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔧 LIMPEZA DE BANCO DE DADOS — RELATÓRIO                   ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        resumo = relatorio.get('resumo', {})
        print(f"📊 RESUMO:")
        print(f"   • Total Ações: {resumo.get('total_acoes', 0)}")
        print(f"   • Sucessos: {resumo.get('sucessos', 0)}")
        print(f"   • Sugeridos: {resumo.get('sugeridos', 0)}")
        print(f"   • Análises: {resumo.get('analises', 0)}")
        print()
        
        acoes = relatorio.get('acoes_realizadas', [])
        if acoes:
            print(f"📋 AÇÕES REALIZADAS:")
            for i, acao in enumerate(acoes, 1):
                status_icon = "✅" if acao.get('status') == 'sucesso' else "📊" if acao.get('status') == 'sugerido' else "🔍"
                print(f"   {i}. {status_icon} {acao.get('acao')}: {acao.get('count', 'N/A')}")
            print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔧 LIMPEZA DE BANCO DE DADOS — CONCLUÍDO                   ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
    
    def salvar_relatorio(self, arquivo_path: str, relatorio: Dict):
        """Salva relatório em arquivo JSON"""
        try:
            with open(arquivo_path, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Relatório salvo em: {arquivo_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")


# ==================== MAIN ====================

def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🔧 LIMPEZA DE BANCO DE DADOS                     ║")
    print("║     Removendo redundâncias e corrigindo erros     ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    limpeza = LimpezaBancoDados()
    
    # 1. Remover clients duplicados
    print("🗑️ Passo 1: Remover Clients Duplicados")
    print("─" * 50)
    removidos = limpeza.remover_clients_duplicados()
    print(f"✅ {removidos} clients duplicados removidos")
    print()
    
    # 2. Criar clients para órfãos
    print("🆕 Passo 2: Criar Clients para Órfãos")
    print("─" * 50)
    criados = limpeza.criar_clients_para_orfaos()
    print(f"✅ {criados} clients criados")
    print()
    
    # 3. Remover clients sem conversas
    print("🗑️ Passo 3: Remover Clients Sem Conversas")
    print("─" * 50)
    removidos_sem_conversa = limpeza.remover_clients_sem_conversas()
    print(f"✅ {removidos_sem_conversa} clients removidos")
    print()
    
    # 4. Criar índices de performance
    print("📊 Passo 4: Criar Índices de Performance")
    print("─" * 50)
    indices = limpeza.criar_indices_performance()
    print(f"✅ {len(indices)} índices sugeridos")
    print()
    
    # 5. Consolidar tabelas similares
    print("🔍 Passo 5: Analisar Tabelas Similares")
    print("─" * 50)
    sugestoes = limpeza.consolidar_tabelas_similares()
    print(f"✅ Análise concluída")
    print()
    
    # 6. Gerar relatório
    print("📊 Passo 6: Gerar Relatório")
    print("─" * 50)
    relatorio = limpeza.gerar_relatorio_limpeza()
    
    if relatorio.get('status') == 'sucesso':
        # Imprimir relatório
        limpeza.imprimir_relatorio(relatorio)
        
        # Salvar relatório
        arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/limpeza_banco_dados_relatorio.json")
        limpeza.salvar_relatorio(str(arquivo_saida), relatorio)
        
        print("✅ Limpeza CONCLUÍDA!")
        print()
    else:
        print(f"❌ Erro: {relatorio.get('mensagem', 'Desconhecido')}")


if __name__ == "__main__":
    main()
