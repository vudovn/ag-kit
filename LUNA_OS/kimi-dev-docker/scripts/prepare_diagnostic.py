import os
import json

# Configuração do Diagnóstico
TARGET_DIR = "/app/luna_os_to_diagnose"
DIAGNOSTIC_GOAL = """
Realizar um diagnóstico profundo no backend do LUNA OS (FastAPI).
Foco: 
1. Identificar redundâncias na lógica do BrainEngine.
2. Sugerir refatoração para melhor separação de interesses.
3. Verificar segurança nos webhooks da Evolution API.
"""


def create_diagnostic_task():
    print(f"🔍 Preparando diagnóstico para: {TARGET_DIR}")

    # Kimi-Dev geralmente espera uma estrutura de 'issue' ou 'problem statement'
    # Vamos criar um arquivo de contexto para o agente
    task_file = "/app/scripts/luna_diagnostic_issue.json"

    issue_data = {
        "issue_id": "LUNA-REFAC-001",
        "description": DIAGNOSTIC_GOAL,
        "repo_path": TARGET_DIR,
    }

    with open(task_file, "w") as f:
        json.dump(issue_data, f, indent=4)

    print(f"✅ Issue de diagnóstico criada: {task_file}")
    print("\n🚀 COMANDO PARA EXECUTAR O KIMI-DEV:")
    print(
        f"python3 kimidev/examples/rollout_messages_bugfixer.py --model_name llama3.2 --issue_file {task_file}"
    )


if __name__ == "__main__":
    create_diagnostic_task()
