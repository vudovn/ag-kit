import json
import os
import sys
import re

# Garantir que o diretório do kimidev está no path
sys.path.append("/app")

from kimidev.agentlessnano.model_api import make_model
from kimidev.agentlessnano.utils import show_project_structure

# Configurações do Ambiente
os.environ["PROJECT_FILE_LOC"] = "/app/repo_structures"
MODEL_NAME = "llama3.2"
ISSUE_FILE = "/app/scripts/luna_diagnostic_issue.json"
REPO_JSON = "/app/repo_structures/luna__luna-os.json"
BASE_REPO_PATH = "/app/luna_os_to_diagnose"


def llm_chat(model, prompt):
    """Simula a função llm_chat utilizada nos scripts do Kimi-Dev"""
    trajs = model.codegen(prompt)
    if not trajs:
        return None, ""
    return trajs[0], trajs[0].get("response", "")


def run_diagnostic():
    print("🚀 Iniciando Diagnóstico LUNA OS via Kimi-Dev (Motor: Llama)...")

    if not os.path.exists(ISSUE_FILE):
        print(f"❌ Erro: Arquivo de issue não encontrado em {ISSUE_FILE}")
        return

    with open(ISSUE_FILE, "r") as f:
        issue = json.load(f)

    with open(REPO_JSON, "r") as f:
        repo_data = json.load(f)
        structure = repo_data["structure"]

    # Inicializa o modelo configurado para o Ollama host
    llm_model = make_model(model=MODEL_NAME, backend="kimidev")

    problem_description = issue["description"]

    # --- ETAPA 1: LOCALIZAÇÃO DE ARQUIVOS CRÍTICOS ---
    print("\n🔎 Etapa 1: Kimi está escaneando a estrutura do repositório...")

    obtain_relevant_files_prompt = """
    Please look through the following Repository structure and provide a list of files that one would need to edit or refactor to solve the problem description.

    ### PROBLEM DESCRIPTION ###
    {problem_statement}

    ### REPOSITORY STRUCTURE ###
    {structure}

    ###
    Please only provide the full path of the files. Return at most 10 relevant files.
    Separate files by new lines and wrap them with ```
    """

    struct_view = show_project_structure(structure).strip()
    prompt_loc = obtain_relevant_files_prompt.format(
        problem_statement=problem_description, structure=struct_view
    )

    _, raw_files_answer = llm_chat(llm_model, prompt_loc)
    print(f"✅ Kimi identificou os seguintes arquivos como críticos para o LUNA OS:")

    # Extrair caminhos dos arquivos
    found_files = []
    # Busca blocos de código
    matches = re.findall(r"```(?:\w+)?\n?(.*?)\n?```", raw_files_answer, re.DOTALL)
    content_to_parse = matches[0] if matches else raw_files_answer

    for line in content_to_parse.split("\n"):
        f = line.strip().replace("- ", "").replace("* ", "")
        if f and (f.endswith(".py") or f.endswith(".ts") or f.endswith(".tsx")):
            found_files.append(f)

    # Filtrar apenas os que realmente existem
    valid_files = []
    for f in list(set(found_files)):
        full_p = os.path.join(BASE_REPO_PATH, f)
        if os.path.exists(full_p):
            valid_files.append(f)

    print(f"📊 {len(valid_files)} arquivos validados para análise profunda.")

    if not valid_files:
        print("⚠️ Nenhum arquivo válido encontrado para análise. Abortando.")
        return

    # --- ETAPA 2: ANÁLISE E DIAGNÓSTICO ---
    print("\n🧐 Etapa 2: Kimi está realizando a análise profunda dos arquivos...")

    all_code_content = ""
    for f_path in valid_files[:8]:  # Limite para não estourar contexto
        # No Kimi-Dev real, ele usaria um skeleton. Aqui vamos ler o conteúdo.
        abs_p = os.path.join(BASE_REPO_PATH, f_path)
        with open(abs_p, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
            all_code_content += f"\nFILE: {f_path}\n```python\n{code}\n```\n"

    diagnostic_prompt = """
    You are the Kimi-Dev Architect. Your goal is to provide a deep diagnostic for refactoring and improvement.
    
    ### GOAL ###
    {problem_statement}
    
    ### CODE CONTEXT ###
    {content}
    
    ### TASK ###
    Based on the code provided, generate a MASTER DIAGNOSTIC REPORT in Portuguese.
    Identify:
    1. MODULARIDADE: Onde a lógica está muito acoplada (BrainEngine vs Handlers)?
    2. REDUNDÂNCIA: Existem funções fazendo a mesma coisa?
    3. SEGURANÇA: Os webhooks e APIs estão protegidos contra exposição de dados?
    4. MELHORIAS: Sugestões concretas de refatoração.
    
    Format the output in clean Markdown.
    """

    prompt_diag = diagnostic_prompt.format(
        problem_statement=problem_description, content=all_code_content
    )

    _, final_report = llm_chat(llm_model, prompt_diag)

    # Salvar Relatório
    report_path = "/app/scripts/luna_diagnostic_report.md"
    with open(report_path, "w") as f:
        f.write("# ☄️ RELATÓRIO DE DIAGNÓSTICO LUNA OS - KIMI-DEV\n\n")
        f.write(final_report)

    print(f"🏆 Diagnóstico concluído com sucesso!")
    print(f"📄 Relatório salvo em: {report_path}")
    print("\n--- PRÓXIMO PASSO ---")
    print(
        "Mova o relatório para o Atlas Soberano ou aplique as refatorações sugeridas."
    )


if __name__ == "__main__":
    run_diagnostic()
