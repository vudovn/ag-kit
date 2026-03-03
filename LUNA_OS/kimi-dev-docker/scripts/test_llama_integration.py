import openai
import os

# Configurações para Ollama via Host (Docker bridge)
# No Mac, host.docker.internal aponta para a máquina hospedeira
client = openai.OpenAI(
    base_url="http://host.docker.internal:11434/v1",
    api_key="ollama",  # Ollama não exige chave real
)

print("🧪 Testando integração Kimi-Dev <> Llama (Ollama)...")

try:
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "Você é o motor de inferência do Kimi-Dev."},
            {
                "role": "user",
                "content": "Olá, você está pronto para resolver issues de código?",
            },
        ],
    )
    print("\n✅ Resposta do Llama:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\n❌ Erro na integração: {e}")
    print("Tentando via localhost caso network_mode: host esteja ativo...")
    try:
        client.base_url = "http://localhost:11434/v1"
        response = client.chat.completions.create(
            model="llama3.2", messages=[{"role": "user", "content": "teste"}]
        )
        print("✅ Sucesso via localhost!")
    except Exception as e2:
        print(f"❌ Falha total: {e2}")
