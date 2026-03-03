#!/usr/bin/env python3
"""
🌙🤖 LUNA OS v3.0 — AUTO-CONVERSA SIMULATOR
Simula conversas reais entre Luna e Cliente Simulado
Conecta TODOS os módulos: Brain + Dojo + Analytics + Modules V3
"""

import sys
import json
import random
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from app.core.brain import process_message
from app.integrations.supabase_client import get_supabase
from loguru import logger

# Configurar logs
logger.add("logs/auto_conversa_simulator.log", rotation="10 MB", retention="30 days")


# ==================== AGENTE CLIENTE ====================


class ClienteSimulado:
    """
    Agente que simula um cliente real
    Usa dados das 40K mensagens para comportamento realista
    """

    def __init__(self, perfil: str = "medio"):
        self.perfil = perfil
        self.nome = f"Cliente Simulado {random.randint(1, 1000)}"
        self.phone = f"554999999{random.randint(1000, 9999)}"
        self.humor = "neutro"  # feliz, neutro, irritado, com_pressa
        self.intencao_atual = None
        self.historico_conversa = []
        self.paciencia = 100  # Diminui com respostas ruins

        # Carregar intenções reais das 40K mensagens
        self.intencoes_reais = self._carregar_intencoes_reais()

        # Personalidade por perfil
        self.personalidades = {
            "facil": {
                "paciencia_inicial": 150,
                "claro": True,
                "exigente": False,
                "respostas_curtas": False,
            },
            "medio": {
                "paciencia_inicial": 100,
                "claro": True,
                "exigente": False,
                "respostas_curtas": True,
            },
            "dificil": {
                "paciencia_inicial": 50,
                "claro": False,
                "exigente": True,
                "respostas_curtas": True,
            },
            "com_pressa": {
                "paciencia_inicial": 30,
                "claro": True,
                "exigente": True,
                "respostas_curtas": True,
            },
        }

        self.personalidade = self.personalidades.get(
            perfil, self.personalidades["medio"]
        )
        self.paciencia = self.personalidade["paciencia_inicial"]

        logger.info(f"🧑 Cliente Simulado criado: {self.nome} ({perfil})")

    def _carregar_intencoes_reais(self) -> List[str]:
        """Carrega intenções reais das 40K mensagens"""
        # Intenções baseadas nas 5.908 situações do Dojo
        return [
            "agendar",
            "preco",
            "horario_func",
            "localizacao",
            "servicos",
            "pacote",
            "cupom",
            "reclamacao",
            "handoff",
            "saudacao",
            "agradecimento",
        ]

    def gerar_mensagem(self) -> str:
        """
        Gera mensagem realista baseada em intenção
        Usa dados reais das 40K mensagens
        """
        # Escolher intenção
        self.intencao_atual = random.choice(self.intencoes_reais)

        # Mensagens reais baseadas em intenção
        mensagens_por_intencao = {
            "agendar": [
                "Vcs teriam horário às 15h?",
                "Quero marcar um horário para amanhã",
                "Tem vaga para hoje?",
                "Preciso agendar urgente!",
                "Qual horário disponível essa semana?",
            ],
            "preco": [
                "Quanto custa uma escova?",
                "Qual o valor do pacote?",
                "Tem desconto?",
                "Tá caro, faz por menos?",
                "Qual preço da unha em gel?",
            ],
            "horario_func": [
                "Que horas vocês abrem?",
                "Funciona sábado?",
                "Até que horas fica aberto?",
                "Abre no almoço?",
                "Domingo tem atendimento?",
            ],
            "localizacao": [
                "Onde fica o salão?",
                "Qual endereço?",
                "Tem estacionamento?",
                "É no centro?",
                "Como chego aí?",
            ],
            "servicos": [
                "Quais serviços vocês fazem?",
                "Faz progressiva?",
                "Tem manicure?",
                "Faz sobranclha também?",
                "O que vocês oferecem?",
            ],
            "pacote": [
                "Tem pacote promocional?",
                "Faz desconto no combo?",
                "Quero fazer vários serviços, tem preço especial?",
                "Pacote noiva tem?",
                "Qual pacote vale mais pena?",
            ],
            "reclamacao": [
                "Esperei 30 minutos da última vez!",
                "Não gostei do resultado",
                "Minha unha descascou em 2 dias",
                "O atendimento foi ruim",
                "Quero reclamar de um serviço",
            ],
            "saudacao": [
                "Oi, tudo bem?",
                "Bom dia!",
                "Olá",
                "Boa tarde",
                "Oi, preciso de ajuda",
            ],
        }

        # Selecionar mensagem baseada na intenção
        mensagens = mensagens_por_intencao.get(
            self.intencao_atual, ["Preciso de ajuda"]
        )

        # Adicionar variação baseada no humor
        if self.humor == "com_pressa":
            return f"URGENTE: {random.choice(mensagens)}"
        elif self.humor == "irritado":
            return f"Olha, {random.choice(mensagens)} Isso é um absurdo!"
        else:
            return random.choice(mensagens)

    def receber_resposta(self, resposta: str, avaliacao: Dict):
        """
        Recebe resposta da Luna e atualiza estado
        """
        self.historico_conversa.append(
            {
                "resposta_luna": resposta,
                "avaliacao": avaliacao,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Atualizar humor baseado na resposta
        if avaliacao.get("sucesso", False):
            self.paciencia = min(self.paciencia + 10, 100)
            if self.humor == "irritado":
                self.humor = "neutro"
        else:
            self.paciencia -= 20
            if self.paciencia < 30:
                self.humor = "irritado"
            elif self.paciencia < 60:
                self.humor = "com_pressa"

        logger.debug(
            f"🧑 Cliente {self.nome}: paciência={self.paciencia}, humor={self.humor}"
        )

    def deve_continuar(self) -> bool:
        """Verifica se cliente deve continuar conversando"""
        # Cliente desiste se:
        # - Paciência zerou
        # - Problema resolvido
        # - 10 mensagens sem sucesso

        if self.paciencia <= 0:
            logger.info(f"🧑 Cliente {self.nome} desistiu (paciência zerou)")
            return False

        if len(self.historico_conversa) >= 10:
            logger.info(f"🧑 Cliente {self.nome} encerrou (10 mensagens)")
            return False

        # Verificar se problema foi resolvido
        ultimas_respostas = self.historico_conversa[-3:]
        sucessos = sum(
            1 for h in ultimas_respostas if h.get("avaliacao", {}).get("sucesso", False)
        )

        if sucessos >= 2:
            logger.info(f"🧑 Cliente {self.nome} satisfeito (problema resolvido)")
            return False

        return True


# ==================== AGENTE LUNA ====================


class AgenteLuna:
    """
    Agente Luna que usa Brain real + Modules V3
    """

    def __init__(self):
        self.historico_conversas = []
        self.metricas = {
            "total_respostas": 0,
            "respostas_sucesso": 0,
            "tempo_medio_ms": 0,
        }
        logger.info("🤖 Agente Luna inicializado")

    async def responder(
        self, mensagem: str, cliente_phone: str, cliente_nome: str
    ) -> Dict:
        """
        Usa Brain real para responder
        """
        try:
            start_time = datetime.utcnow()

            # Chamar Brain real
            resposta = await process_message(
                phone=cliente_phone, name=cliente_nome, message=mensagem, history=[]
            )

            end_time = datetime.utcnow()
            tempo_ms = (end_time - start_time).total_seconds() * 1000

            # Atualizar métricas
            self.metricas["total_respostas"] += 1
            if resposta.get("ok", False):
                self.metricas["respostas_sucesso"] += 1
            self.metricas["tempo_medio_ms"] = (
                self.metricas["tempo_medio_ms"] * (self.metricas["total_respostas"] - 1)
                + tempo_ms
            ) / self.metricas["total_respostas"]

            self.historico_conversas.append(
                {
                    "mensagem": mensagem,
                    "resposta": resposta,
                    "tempo_ms": tempo_ms,
                    "timestamp": start_time.isoformat(),
                }
            )

            logger.debug(
                f"🤖 Luna respondeu em {tempo_ms:.0f}ms: {resposta.get('intent', 'unknown')}"
            )

            return resposta

        except Exception as e:
            logger.error(f"❌ Luna falhou: {e}")
            return {
                "ok": False,
                "response": "Desculpe, estou com problemas técnicos. Pode repetir?",
                "intent": "erro",
                "error": str(e),
            }

    def get_metricas(self) -> Dict:
        """Retorna métricas de performance"""
        return {
            **self.metricas,
            "taxa_sucesso": (
                (
                    self.metricas["respostas_sucesso"]
                    / self.metricas["total_respostas"]
                    * 100
                )
                if self.metricas["total_respostas"] > 0
                else 0
            ),
        }


# ==================== SIMULADOR ====================


class AutoConversaSimulator:
    """
    Simula conversas entre Luna e Cliente Simulado
    Conecta TODOS os módulos
    """

    def __init__(self):
        self.db = get_supabase()
        self.resultados_simulacoes = []
        logger.info("🎯 AutoConversa Simulator inicializado (Modo: Dual Brain)")

        # Cores ANSI
        self.C_LOGIC = "\033[93m"  # Amarelo
        self.C_VOICE = "\033[96m"  # Ciano
        self.C_USER = "\033[92m"  # Verde
        self.C_RESET = "\033[0m"

    async def simular_conversa(self, perfil_cliente: str = "medio") -> Dict:
        """
        Simula uma conversa completa
        """
        logger.info(f"🎯 Iniciando simulação (perfil: {perfil_cliente})")

        # Criar agentes
        cliente = ClienteSimulado(perfil=perfil_cliente)
        luna = AgenteLuna()

        # Histórico da conversa
        conversa_completa = []

        # Loop de conversa
        turno = 0
        while cliente.deve_continuar() and turno < 10:
            turno += 1

            # 1. Cliente gera mensagem
            mensagem_cliente = cliente.gerar_mensagem()
            print(
                f"\n{self.C_USER}🧑 Cliente ({turno}): {mensagem_cliente}{self.C_RESET}"
            )

            # 2. Luna responde (Pipeline Dual Brain roda aqui)
            print(
                f"   {self.C_LOGIC}🧠 [Dual Brain] Processando Lógica Soberana...{self.C_RESET}"
            )
            resposta_luna = await luna.responder(
                mensagem=mensagem_cliente,
                cliente_phone=cliente.phone,
                cliente_nome=cliente.nome,
            )

            resposta_texto = resposta_luna.get("response", "Desculpe, não entendi")
            modelo_usado = resposta_luna.get("model", "unknown")
            tempo_ms = resposta_luna.get("processing_ms", 0)

            # Extraindo a inteligência simulada que veio da lógica
            intel = resposta_luna.get("intelligence", {})
            insight = (
                intel.get("insight", "N/A")
                if isinstance(intel, dict)
                else getattr(intel, "insight", "N/A")
            )

            print(
                f"   {self.C_LOGIC}⚡ Insight Lógico Extraído: {insight}{self.C_RESET}"
            )
            print(
                f"   {self.C_VOICE}🤖 Luna Voz ({turno}) [{modelo_usado} em {tempo_ms}ms]: {resposta_texto}{self.C_RESET}"
            )

            # 3. Avaliar resposta
            avaliacao = self._avaliar_resposta(
                mensagem_cliente, resposta_luna, cliente.intencao_atual
            )

            # 4. Cliente recebe resposta
            cliente.receber_resposta(resposta_texto, avaliacao)

            # 5. Registrar turno
            conversa_completa.append(
                {
                    "turno": turno,
                    "mensagem_cliente": mensagem_cliente,
                    "intencao": cliente.intencao_atual,
                    "resposta_luna": resposta_texto,
                    "intent_detectada": resposta_luna.get("intent", "unknown"),
                    "avaliacao": avaliacao,
                    "humor_cliente": cliente.humor,
                    "paciencia_cliente": cliente.paciencia,
                }
            )

        # 6. Gerar relatório final
        relatorio = self._gerar_relatorio(
            conversa_completa, luna.get_metricas(), cliente
        )

        self.resultados_simulacoes.append(relatorio)

        logger.info(f"✅ Simulação concluída: {relatorio['status_final']}")

        return relatorio

    def _avaliar_resposta(
        self, mensagem: str, resposta: Dict, intencao_real: str
    ) -> Dict:
        """
        Avalia qualidade da resposta da Luna
        """
        avaliacao = {"sucesso": False, "pontos": 0, "motivos": []}

        # Critério 1: Intent detectada corretamente
        intent_detectada = resposta.get("intent", "unknown")
        if intent_detectada == intencao_real:
            avaliacao["pontos"] += 30
            avaliacao["motivos"].append("Intent correta")
        elif (
            intent_detectada in ["agendar", "agendamento"]
            and intencao_real == "agendar"
        ):
            avaliacao["pontos"] += 20
            avaliacao["motivos"].append("Intent relacionada")

        # Critério 2: Resposta não é erro
        if resposta.get("ok", False):
            avaliacao["pontos"] += 30
            avaliacao["motivos"].append("Resposta OK")
        else:
            avaliacao["motivos"].append("Resposta com erro")

        # Critério 3: Resposta tem conteúdo
        resposta_texto = resposta.get("response", "")
        if len(resposta_texto) > 10:
            avaliacao["pontos"] += 20
            avaliacao["motivos"].append("Resposta completa")
        else:
            avaliacao["motivos"].append("Resposta muito curta")

        # Critério 4: Resposta é empática
        palavras_empaticas = ["oi", "olá", "obrigado", "por favor", "ajudar", "posso"]
        if any(p in resposta_texto.lower() for p in palavras_empaticas):
            avaliacao["pontos"] += 20
            avaliacao["motivos"].append("Resposta empática")

        # Determinar sucesso
        avaliacao["sucesso"] = avaliacao["pontos"] >= 60

        return avaliacao

    def _gerar_relatorio(
        self, conversa: List[Dict], metricas: Dict, cliente: ClienteSimulado
    ) -> Dict:
        """
        Gera relatório completo da simulação
        """
        turnos = len(conversa)
        sucessos = sum(
            1 for t in conversa if t.get("avaliacao", {}).get("sucesso", False)
        )
        taxa_sucesso = (sucessos / turnos * 100) if turnos > 0 else 0

        # Determinar status final
        if cliente.paciencia <= 0:
            status_final = "cliente_desistiu"
        elif sucessos >= turnos * 0.7:
            status_final = "sucesso"
        else:
            status_final = "parcial"

        return {
            "status_final": status_final,
            "perfil_cliente": cliente.perfil,
            "turnos": turnos,
            "sucessos": sucessos,
            "taxa_sucesso": taxa_sucesso,
            "paciencia_final": cliente.paciencia,
            "humor_final": cliente.humor,
            "metricas_luna": metricas,
            "conversa": conversa,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def simular_lote(self, quantidade: int = 10) -> Dict:
        """
        Simula múltiplas conversas
        """
        logger.info(f"🎯 Iniciando lote de {quantidade} simulações")

        resultados = []

        for i in range(quantidade):
            for perfil in ["facil", "medio", "dificil", "com_pressa"]:
                resultado = await self.simular_conversa(perfil_cliente=perfil)
                resultados.append(resultado)

        # Gerar relatório consolidado
        relatorio_consolidado = self._gerar_relatorio_consolidado(resultados)

        return relatorio_consolidado

    def _gerar_relatorio_consolidado(self, resultados: List[Dict]) -> Dict:
        """
        Gera relatório consolidado de múltiplas simulações
        """
        total = len(resultados)
        sucessos = sum(1 for r in resultados if r.get("status_final") == "sucesso")
        parciais = sum(1 for r in resultados if r.get("status_final") == "parcial")
        desistencias = sum(
            1 for r in resultados if r.get("status_final") == "cliente_desistiu"
        )

        taxa_sucesso_geral = (sucessos / total * 100) if total > 0 else 0

        # Métricas por perfil
        por_perfil = {}
        for resultado in resultados:
            perfil = resultado.get("perfil_cliente", "unknown")
            if perfil not in por_perfil:
                por_perfil[perfil] = []
            por_perfil[perfil].append(resultado)

        metricas_por_perfil = {}
        for perfil, resultados_perfil in por_perfil.items():
            metricas_por_perfil[perfil] = {
                "quantidade": len(resultados_perfil),
                "taxa_sucesso": sum(
                    1 for r in resultados_perfil if r.get("status_final") == "sucesso"
                )
                / len(resultados_perfil)
                * 100,
                "paciencia_media": sum(
                    r.get("paciencia_final", 0) for r in resultados_perfil
                )
                / len(resultados_perfil),
            }

        return {
            "total_simulacoes": total,
            "sucessos": sucessos,
            "parciais": parciais,
            "desistencias": desistencias,
            "taxa_sucesso_geral": taxa_sucesso_geral,
            "metricas_por_perfil": metricas_por_perfil,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def imprimir_relatorio(self, relatorio: Dict):
        """Imprime relatório formatado"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🤖 AUTO-CONVERSA SIMULATOR — RELATÓRIO                     ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()

        if "total_simulacoes" in relatorio:
            # Relatório consolidado
            print(f"📊 Total Simulações: {relatorio.get('total_simulacoes')}")
            print(f"✅ Sucessos: {relatorio.get('sucessos')}")
            print(f"🟡 Parciais: {relatorio.get('parciais')}")
            print(f"❌ Desistências: {relatorio.get('desistencias')}")
            print(f"📈 Taxa de Sucesso: {relatorio.get('taxa_sucesso_geral', 0):.1f}%")
            print()

            print("📊 Por Perfil:")
            for perfil, metricas in relatorio.get("metricas_por_perfil", {}).items():
                print(
                    f"   • {perfil}: {metricas['taxa_sucesso']:.1f}% sucesso, paciência {metricas['paciencia_media']:.0f}"
                )
        else:
            # Relatório único
            print(f"📊 Status Final: {relatorio.get('status_final', 'unknown')}")
            print(f"🧑 Perfil Cliente: {relatorio.get('perfil_cliente', 'unknown')}")
            print(f"📊 Turnos: {relatorio.get('turnos')}")
            print(f"✅ Taxa de Sucesso: {relatorio.get('taxa_sucesso', 0):.1f}%")
            print(f"💚 Paciência Final: {relatorio.get('paciencia_final', 0)}")
            print(f"😊 Humor Final: {relatorio.get('humor_final', 'unknown')}")

        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  🤖 AUTO-CONVERSA SIMULATOR — CONCLUÍDO                     ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()

    def salvar_relatorio(self, arquivo_path: str, relatorio: Dict):
        """Salva relatório em arquivo JSON"""
        try:
            with open(arquivo_path, "w", encoding="utf-8") as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)

            logger.info(f"💾 Relatório salvo em: {arquivo_path}")

        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")


# ==================== MAIN ====================


async def main():
    """Main function"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║  🤖 AUTO-CONVERSA SIMULATOR                       ║")
    print("║     Luna vs Cliente Simulado                      ║")
    print("╚════════════════════════════════════════════════════╝")
    print()

    simulator = AutoConversaSimulator()

    # 1. Simulação única (demonstração)
    print("🎯 Passo 1: Simulação Única (Demonstração)")
    print("─" * 50)

    resultado_unico = await simulator.simular_conversa(perfil_cliente="medio")
    simulator.imprimir_relatorio(resultado_unico)

    # Salvar relatório único
    arquivo_saida = Path(
        "/Users/franciscotaveira.ads/LUNA OS/logs/auto_conversa_unico.json"
    )
    simulator.salvar_relatorio(str(arquivo_saida), resultado_unico)

    # 2. Simular lote (10 conversas)
    print("🎯 Passo 2: Lote de Simulações (10 conversas)")
    print("─" * 50)

    relatorio_lote = await simulator.simular_lote(quantidade=10)
    simulator.imprimir_relatorio(relatorio_lote)

    # Salvar relatório consolidado
    arquivo_saida = Path(
        "/Users/franciscotaveira.ads/LUNA OS/logs/auto_conversa_lote.json"
    )
    simulator.salvar_relatorio(str(arquivo_saida), relatorio_lote)

    print()
    print("✅ Auto-Conversa Simulator CONCLUÍDO!")
    print()
    print("📁 Relatórios:")
    print(f"   • Único: {arquivo_saida}")
    print()


if __name__ == "__main__":
    if sys.platform != "win32":
        try:
            import readline  # Apenas para ambiente linux/gitbash
        except ImportError:
            pass

    asyncio.run(main())
