"""
Anthropic Claude Integration
"""
import anthropic
import httpx
from app.config import settings

class ClaudeAPI:
    def __init__(self):
        self.use_openrouter = bool(settings.openrouter_key)
        
        if self.use_openrouter:
            self.base_url = "https://openrouter.ai/api/v1/chat/completions"
            self.api_key = settings.openrouter_key
        else:
            self.client = anthropic.Anthropic(api_key=settings.anthropic_key)
    
    async def complete(
        self,
        messages: list,
        system: str = "",
        model: str = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """Generate completion"""
        model = model or settings.model_quick
        
        if self.use_openrouter:
            return await self._openrouter_complete(messages, system, model, max_tokens, temperature)
        else:
            return await self._anthropic_complete(messages, system, model, max_tokens, temperature)
    
    async def _anthropic_complete(self, messages, system, model, max_tokens, temperature):
        """Direct Anthropic API"""
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages
        )
        return response.content[0].text
    
    async def _openrouter_complete(self, messages, system, model, max_tokens, temperature):
        """OpenRouter API"""
        # Prepend system message
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)
        
        # Map model names
        model_map = {
            "claude-3-haiku-20240307": "anthropic/claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022": "anthropic/claude-3-5-sonnet-20241022"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://haven.mct.com.br",
                    "X-Title": "Luna Core"
                },
                json={
                    "model": model_map.get(model, model),
                    "messages": full_messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=60.0
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]

claude = ClaudeAPI()
