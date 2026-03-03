"""
Dojo Simulator — Simulador de conversas para estresse da LUNA
Utiliza Ollama (local) para gerar respostas do cliente.
Integra com o core/brain.py da LUNA.
"""

# WORKAROUND: Fix httpx/gotrue proxy argument mismatch
import httpx

original_init = httpx.Client.__init__


def new_init(self, *args, **kwargs):
    if "proxy" in kwargs:
        kwargs["proxies"] = kwargs.pop("proxy")
    original_init(self, *args, **kwargs)


httpx.Client.__init__ = new_init

import json
import random
import os
import asyncio
from datetime import datetime
from loguru import logger
from app.dojo.scenarios import SCENARIOS
from app.dojo.personas import PERSONAS


class DojoSimulator:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.scenarios = SCENARIOS
        self.personas = PERSONAS
        logger.info(
            f"🥋 Dojo Simulator inicializado com {len(PERSONAS)} personas e {len(SCENARIOS)} cenários"
        )
        logger.info(f"🦙 Ollama: llama3.2 em {ollama_url}")

    async def generate_customer_response(self, persona, context, luna_message):
        """Usa Ollama para gerar a próxima frase do cliente"""
        # Adaptação para os atributos reais das personas
        desc = persona.get("description", persona.get("profile", "Cliente de salão"))
        mood = persona.get("mood", "neutral")

        prompt = f"""
        Você é um cliente de um salão de beleza (Haven Escovaria).
        Sua Persona: {persona['name']} - {desc}
        Humor atual: {mood}
        Contexto da Situação: {context}

        LUNA (Atendente AI) disse: "{luna_message}"

        Como você responde a isso? Seja breve (máximo 2 frases), mantenha sua persona e seu humor.
        NÃO use emojis em excesso. NÃO saia do personagem.
        """

        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9},
        }

        try:
            import httpx

            with httpx.Client(timeout=60.0) as client:
                response = client.post(f"{self.ollama_url}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                customer_message = data["response"].strip().replace('"', "")
                logger.debug(f"🤖 Cliente ({persona['name']}): {customer_message}")
                return customer_message
        except Exception as e:
            logger.error(f"Falha ao gerar resposta: {e}")
            return "Ok, entendi."

    def _check_criterion(self, criterion, luna_message, conversation):
        """Verifica se um critério de sucesso foi atingido"""
        # Simplificado para busca de keywords
        keywords = {
            "identificacao": ["Luna", "Haven"],
            "empatia": ["entendo", "sinto muito", "com certeza", "claro"],
            "proposta_valor": ["exclusivo", "premium", "especialista"],
            "handoff": ["transferindo", "humano", "atendente", "aguarde"],
            "preco_correto": ["R$", "valor", "preço"],
            "ordem_servico": ["primeiro", "depois", "seguida"],
        }

        target = keywords.get(criterion, [])
        for k in target:
            if k.lower() in luna_message.lower():
                return True
        return False

    async def simulate_conversation(self, scenario_id, persona_id, max_turns=6):
        """Simula uma conversa completa"""

        # Buscar scenario e persona
        scenario = next((s for s in self.scenarios if s["id"] == scenario_id), None)
        persona = next((p for p in self.personas if p["id"] == persona_id), None)

        if not scenario or not persona:
            return {"error": "Scenario ou Persona não encontrado"}

        logger.info(f"🥋 Iniciando simulação: {scenario['name']} + {persona['name']}")

        # Estado da conversa
        conversation = []
        success_criteria_met = []

        # Integrar com o Cérebro Real da LUNA
        from app.core.brain import process_message

        # Mensagem inicial do cliente
        customer_message = scenario.get("sample_message", "Oi!")
        conversation.append(
            {
                "direction": "inbound",
                "content": customer_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        # Loop de conversa
        for turn in range(max_turns):
            # LUNA responde
            phone = persona.get("phone") or persona.get("numero") or "5549000000000"

            luna_result = await process_message(
                phone=phone,
                name=persona["name"],
                message=customer_message,
                history=conversation,
            )
            luna_message = luna_result.get("response", "")

            logger.info(f"🌙 LUNA: {luna_message}")

            conversation.append(
                {
                    "direction": "outbound",
                    "content": luna_message,
                    "timestamp": datetime.utcnow().isoformat(),
                    "intent": luna_result.get("intent"),
                }
            )

            # Verificar critérios de sucesso
            for criterion in scenario.get("success_criteria", []):
                if self._check_criterion(criterion, luna_message, conversation):
                    if criterion not in success_criteria_met:
                        success_criteria_met.append(criterion)

            # Cliente responde (Ollama)
            customer_message = await self.generate_customer_response(
                persona=persona,
                context=scenario["description"],
                luna_message=luna_message,
            )

            conversation.append(
                {
                    "direction": "inbound",
                    "content": customer_message,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )

            # Se Luna indicou handoff ou fim de conversa, paramos
            # Handle both Enum and string for intent
            intent = luna_result.get("intent")
            intent_val = intent.value if hasattr(intent, "value") else intent
            if intent_val == "handoff":
                logger.info("🛑 Handoff detectado. Finalizando simulação.")
                break

        # Relatório Final
        total_criteria = len(scenario.get("success_criteria", []))
        score = (
            len(success_criteria_met) / total_criteria if total_criteria > 0 else 1.0
        )
        report = {
            "scenario": scenario["name"],
            "persona": persona["name"],
            "score": score,
            "criteria_met": success_criteria_met,
            "turns": len(conversation) // 2,
            "conversation": conversation,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success" if score >= 0.7 else "fail",
        }

        logger.info(f"📊 Resultado: {report['status'].upper()} (Score: {score:.2f})")

        return report


# Instância global para uso na API
simulator = DojoSimulator()


async def test():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenarios", type=str, help="IDs dos cenários separados por vírgula"
    )
    args = parser.parse_args()

    # Usar instância global
    target_scenarios = []
    if args.scenarios:
        target_scenarios = args.scenarios.split(",")
    else:
        # Default de teste
        target_scenarios = ["scenario_016", "scenario_017"]

    for sc_id in target_scenarios:
        # Pega persona aleatória ou específica
        p_id = "persona_009" if "16" in sc_id else "persona_010"

        result = await simulator.simulate_conversation(
            scenario_id=sc_id, persona_id=p_id, max_turns=5
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(test())
