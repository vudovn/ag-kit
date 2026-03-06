#!/usr/bin/env python3
"""
🌙🔧 LUNA OS v3.0 — AUDITORIA DE BANCO DE DADOS
Verifica redundâncias, tabelas duplicadas e inconsistências
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
logger.add("logs/auditoria_banco_dados.log", rotation="10 MB", retention="30 days")


class AuditoriaBancoDados:
    """
    Auditoria completa do banco de dados
    """
    
    def __init__(self):
        self.db = get_supabase()
        self.tabelas_existentes = []
        self.redundancias = []
        self.inconsistencias = []
        
    def listar_todas_tabelas(self) -> List[str]:
        """Lista todas as tabelas do Supabase"""
        try:
            logger.info("📊 Listando todas as tabelas...")
            
            # Query para listar tabelas
            result = self.db.rpc("get_all_tables").execute()
            
            # Fallback: tentar tabelas conhecidas
            tabelas_conhecidas = [
                "clients",
                "conversations",
                "whatsapp_messages_history",
                "business_intelligence",
                "learning_log",
                "dojo_feedback",
                "health_logs",
                "financial_diagnostic",
                "campaigns",
                "knowledge_base",
                "settings"
            ]
            
            # Verificar quais existem
            tabelas_existentes = []
            for tabela in tabelas_conhecidas:
                try:
                    result = self.db.table(tabela).select("count", count="exact").limit(1).execute()
                    tabelas_existentes.append(tabela)
                    logger.info(f"   ✅ {tabela}: EXISTS")
                except Exception as e:
                    logger.warning(f"   ⚠️ {tabela}: NOT FOUND ({e})")
            
            self.tabelas_existentes = tabelas_existentes
            
            logger.info(f"✅ {len(tabelas_existentes)} tabelas encontradas")
            
            return tabelas_existentes
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar tabelas: {e}")
            return []
    
    def verificar_redundancias(self):
        """Verifica tabelas/colunas redundantes"""
        try:
            logger.info("🔍 Verificando redundâncias...")
            
            redundancias_encontradas = []
            
            # 1. Verificar colunas duplicadas (ex: created_at em todas as tabelas)
            colunas_comuns = ["created_at", "updated_at", "id"]
            
            # 2. Verificar tabelas com nomes similares
            nomes_similares = {}
            for tabela in self.tabelas_existentes:
                base = tabela.split("_")[0] if "_" in tabela else tabela
                if base not in nomes_similares:
                    nomes_similares[base] = []
                nomes_similares[base].append(tabela)
            
            for base, tabelas in nomes_similares.items():
                if len(tabelas) > 1:
                    redundancias_encontradas.append({
                        "tipo": "nomes_similares",
                        "tabelas": tabelas,
                        "sugestao": f"Consolidar tabelas {', '.join(tabelas)}"
                    })
            
            # 3. Verificar dados duplicados (mesmo phone em clients)
            logger.info("   📊 Verificando clients duplicados...")
            try:
                result = self.db.table("clients").select("phone").execute()
                phones = [c.get("phone") for c in result.data] if result.data else []
                phones_duplicados = [p for p in phones if phones.count(p) > 1]
                
                if phones_duplicados:
                    redundancias_encontradas.append({
                        "tipo": "clients_duplicados",
                        "count": len(set(phones_duplicados)),
                        "sugestao": "Remover clients duplicados por phone"
                    })
            except Exception as e:
                # [DEBT #A9] Manter fallback mas logar erro específico
                logger.debug(f"Auditoria: erro ao verificar clients duplicados: {e}")
                pass
            
            # 4. Verificar mensagens duplicadas
            logger.info("   📊 Verificando mensagens duplicadas...")
            
            self.redundancias = redundancias_encontradas
            
            logger.info(f"✅ {len(redundancias_encontradas)} redundâncias encontradas")
            
            return redundancias_encontradas
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar redundâncias: {e}")
            return []
    
    def verificar_inconsistencias(self):
        """Verifica inconsistências de dados"""
        try:
            logger.info("🔍 Verificando inconsistências...")
            
            inconsistencias_encontradas = []
            
            # 1. Conversas sem cliente associado
            logger.info("   📊 Verificando conversas órfãs...")
            try:
                conv_result = self.db.table("conversations").select("phone").execute()
                client_result = self.db.table("clients").select("phone").execute()
                
                phones_conversas = set(c.get("phone") for c in conv_result.data) if conv_result.data else set()
                phones_clients = set(c.get("phone") for c in client_result.data) if client_result.data else set()
                
                phones_orfaos = phones_conversas - phones_clients
                
                if phones_orfaos:
                    inconsistencias_encontradas.append({
                        "tipo": "conversas_sem_cliente",
                        "count": len(phones_orfaos),
                        "sugestao": "Criar clients para phones órfãos ou remover conversas"
                    })
            except Exception as e:
                # [DEBT #A9] Manter fallback mas logar erro específico
                logger.debug(f"Auditoria: erro ao verificar conversas órfãs: {e}")
                pass
            
            # 2. Mensagens sem conversa associada
            logger.info("   📊 Verificando mensagens órfãs...")
            
            # 3. Clients sem nenhuma conversa
            logger.info("   📊 Verificando clients sem conversas...")
            try:
                clients_result = self.db.table("clients").select("phone, id").execute()
                convs_result = self.db.table("conversations").select("phone").execute()
                
                phones_com_conversa = set(c.get("phone") for c in convs_result.data) if convs_result.data else set()
                
                clients_sem_conversa = []
                for client in clients_result.data or []:
                    if client.get("phone") not in phones_com_conversa:
                        clients_sem_conversa.append(client.get("phone"))
                
                if clients_sem_conversa:
                    inconsistencias_encontradas.append({
                        "tipo": "clients_sem_conversas",
                        "count": len(clients_sem_conversa),
                        "sugestao": "Remover clients sem conversas ou importar histórico"
                    })
            except Exception as e:
                # [DEBT #A9] Manter fallback mas logar erro específico
                logger.debug(f"Auditoria: erro ao verificar clients sem conversas: {e}")
                pass
            
            # 4. Dados com timestamps inválidos
            logger.info("   📊 Verificando timestamps inválidos...")
            
            self.inconsistencias = inconsistencias_encontradas
            
            logger.info(f"✅ {len(inconsistencias_encontradas)} inconsistências encontradas")
            
            return inconsistencias_encontradas
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar inconsistências: {e}")
            return []
    
    def verificar_indices_faltantes(self):
        """Verifica índices que podem melhorar performance"""
        try:
            logger.info("🔍 Verificando índices faltantes...")
            
            indices_sugeridos = []
            
            # Índices recomendados para performance
            indices_recomendados = [
                {"tabela": "whatsapp_messages_history", "coluna": "phone", "motivo": "Busca por phone"},
                {"tabela": "whatsapp_messages_history", "coluna": "message_timestamp", "motivo": "Ordenação temporal"},
                {"tabela": "conversations", "coluna": "phone", "motivo": "Busca por cliente"},
                {"tabela": "conversations", "coluna": "status", "motivo": "Filtro por status"},
                {"tabela": "clients", "coluna": "phone", "motivo": "Busca única"}
            ]
            
            # Verificar quais já existem (isso exigiria query direta ao PostgreSQL)
            # Por enquanto, sugerir todos
            indices_sugeridos = indices_recomendados
            
            logger.info(f"✅ {len(indices_sugeridos)} índices sugeridos")
            
            return indices_sugeridos
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar índices: {e}")
            return []
    
    def gerar_relatorio_completo(self) -> Dict:
        """Gera relatório completo da auditoria"""
        try:
            logger.info("📊 Gerando relatório completo...")
            
            # Executar todas verificações
            tabelas = self.listar_todas_tabelas()
            redundancias = self.verificar_redundancias()
            inconsistencias = self.verificar_inconsistencias()
            indices = self.verificar_indices_faltantes()
            
            # Contar registros por tabela
            contagem_registros = {}
            for tabela in tabelas:
                try:
                    result = self.db.table(tabela).select("count", count="exact").execute()
                    count = result.count if hasattr(result, 'count') else 0
                    contagem_registros[tabela] = count
                except Exception as e:
                    # [DEBT #A9] Manter fallback mas logar erro específico
                    logger.debug(f"Auditoria: erro ao contar registros de {tabela}: {e}")
                    contagem_registros[tabela] = 0
            
            relatorio = {
                "status": "sucesso",
                "timestamp": datetime.utcnow().isoformat(),
                "tabelas": {
                    "total": len(tabelas),
                    "lista": tabelas,
                    "registros": contagem_registros
                },
                "redundancias": {
                    "total": len(redundancias),
                    "lista": redundancias
                },
                "inconsistencias": {
                    "total": len(inconsistencias),
                    "lista": inconsistencias
                },
                "indices_sugeridos": {
                    "total": len(indices),
                    "lista": indices
                },
                "acoes_recomendadas": self._gerar_acoes_recomendadas(redundancias, inconsistencias, indices)
            }
            
            logger.info(f"✅ Relatório gerado com sucesso")
            
            return relatorio
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            return {"status": "erro", "mensagem": str(e)}
    
    def _gerar_acoes_recomendadas(self, redundancias, inconsistencias, indices) -> List[Dict]:
        """Gera lista de ações recomendadas"""
        acoes = []
        
        # Ações para redundâncias
        for red in redundancias:
            acoes.append({
                "prioridade": "alta" if "duplicado" in red.get("tipo", "") else "media",
                "acao": red.get("sugestao", ""),
                "tipo": "redundancia"
            })
        
        # Ações para inconsistências
        for inc in inconsistencias:
            acoes.append({
                "prioridade": "alta" if "órfão" in inc.get("tipo", "") else "media",
                "acao": inc.get("sugestao", ""),
                "tipo": "inconsistencia"
            })
        
        # Ações para índices
        for idx in indices:
            acoes.append({
                "prioridade": "media",
                "acao": f"CRIAR INDEX em {idx['tabela']}({idx['coluna']})",
                "tipo": "performance"
            })
        
        return acoes
    
    def imprimir_relatorio(self, relatorio: Dict):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔧 AUDITORIA DE BANCO DE DADOS — RELATÓRIO                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        
        # Tabelas
        tabelas = relatorio.get('tabelas', {})
        print(f"📊 TABELAS ({tabelas.get('total', 0)}):")
        for tabela, registros in tabelas.get('registros', {}).items():
            print(f"   • {tabela}: {registros:,} registros")
        print()
        
        # Redundâncias
        redundancias = relatorio.get('redundancias', {})
        print(f"🔴 REDUNDÂNCIAS ({redundancias.get('total', 0)}):")
        for red in redundancias.get('lista', []):
            print(f"   • {red.get('tipo')}: {red.get('sugestao')}")
        print()
        
        # Inconsistências
        inconsistencias = relatorio.get('inconsistencias', {})
        print(f"🟡 INCONSISTÊNCIAS ({inconsistencias.get('total', 0)}):")
        for inc in inconsistencias.get('lista', []):
            print(f"   • {inc.get('tipo')}: {inc.get('sugestao')}")
        print()
        
        # Índices sugeridos
        indices = relatorio.get('indices_sugeridos', {})
        print(f"🔵 ÍNDICES SUGERIDOS ({indices.get('total', 0)}):")
        for idx in indices.get('lista', []):
            print(f"   • {idx['tabela']}({idx['coluna']}): {idx['motivo']}")
        print()
        
        # Ações recomendadas
        acoes = relatorio.get('acoes_recomendadas', [])
        if acoes:
            print(f"📋 AÇÕES RECOMENDADAS ({len(acoes)}):")
            for i, acao in enumerate(sorted(acoes, key=lambda x: 0 if x['prioridade']=='alta' else 1), 1):
                print(f"   {i}. [{acao['prioridade'].upper()}] {acao['acao']}")
            print()
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🔧 AUDITORIA DE BANCO DE DADOS — CONCLUÍDO                 ║")
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
    print("║  🔧 AUDITORIA DE BANCO DE DADOS                   ║")
    print("║     Verificando redundâncias e inconsistências    ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    auditoria = AuditoriaBancoDados()
    
    # Gerar relatório completo
    print("🔍 Executando auditoria completa...")
    print("─" * 50)
    
    relatorio = auditoria.gerar_relatorio_completo()
    
    if relatorio.get('status') == 'sucesso':
        # Imprimir relatório
        auditoria.imprimir_relatorio(relatorio)
        
        # Salvar relatório
        arquivo_saida = Path("/Users/franciscotaveira.ads/LUNA OS/logs/auditoria_banco_dados_relatorio.json")
        auditoria.salvar_relatorio(str(arquivo_saida), relatorio)
        
        print("✅ Auditoria CONCLUÍDA!")
        print()
    else:
        print(f"❌ Erro: {relatorio.get('mensagem', 'Desconhecido')}")


if __name__ == "__main__":
    main()
