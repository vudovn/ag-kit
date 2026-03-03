"""
Brain Structurer Service — Text-to-JSON Intelligence
Converte linguagem natural em dados estruturados para o Brain da Luna.
"""

import json
import re
from app.config import settings
from app.integrations.openrouter import openrouter
from typing import Dict, Any, Optional

SYSTEM_PROMPT = """
Você é o Engenheiro de Dados da LUNA OS. Sua tarefa é converter descrições em linguagem natural em objetos JSON puramente estruturados.

REGRAS:
1. Retorne APENAS o JSON. Sem explicações, sem markdown (proibido usar ```json).
2. Se o texto for sobre HORÁRIOS, use o formato: {"monday": {"open": "HH:MM", "close": "HH:MM"}, ...}
3. Se for sobre SERVIÇOS, use: {"name": "...", "price": 0.0, "duration": 0, "description": "..."} ou uma lista de tais objetos.
4. Se for sobre CONTATO/ENDEREÇO, use chaves claras como "phone", "whatsapp", "address", "city", "zip".
5. Se for uma regra geral ou FAQ, use: {"content": "O texto formatado de forma limpa"}.
6. Use nomes de chaves em inglês para manter o padrão técnico do código-fonte.

EXEMPLO INPUT: "Abrimos de segunda a sabado das 8 as 20"
EXEMPLO OUTPUT: {"monday": {"open": "08:00", "close": "20:00"}, "tuesday": {"open": "08:00", "close": "20:00"}, "wednesday": {"open": "08:00", "close": "20:00"}, "thursday": {"open": "08:00", "close": "20:00"}, "friday": {"open": "08:00", "close": "20:00"}, "saturday": {"open": "08:00", "close": "20:00"}, "sunday": "closed"}
"""


class BrainStructurer:
    async def structure(
        self, text: str, category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia o texto para a OpenRouter e extrai o JSON estruturado.
        """
        prompt = f"Converta o seguinte texto para JSON estruturado{' na categoria ' + category if category else ''}:\n\n{text}"

        try:
            # Assuming self.client is initialized elsewhere to be the openrouter client
            # And 'messages' is meant to be the list of messages for the API call
            messages = [{"role": "user", "content": prompt}]
            raw_response = await openrouter.complete(  # Changed from self.client.complete to openrouter.complete to match original import
                messages,
                model=settings.model_complex,
                system=SYSTEM_PROMPT,
                temperature=0.1,
            )

            # Limpeza de possíveis artefatos de fencas (Markdown)
            clean_json = re.sub(r"```json\s*|\s*```", "", raw_response).strip()

            return json.loads(clean_json)
        except Exception as e:
            # Fallback para objeto simples se a IA falhar no JSON
            return {"content": text, "error": "AI_PARSE_FAILED", "detail": str(e)}


brain_structurer = BrainStructurer()
