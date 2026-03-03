import os
import ast
import json


def get_class_function_info(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.splitlines()

        tree = ast.parse(content)

        classes = []
        functions = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                classes.append(
                    {
                        "name": node.name,
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "text": lines[
                            node.lineno - 1 : getattr(node, "end_lineno", node.lineno)
                        ],
                    }
                )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(
                    {
                        "name": node.name,
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "text": lines[
                            node.lineno - 1 : getattr(node, "end_lineno", node.lineno)
                        ],
                    }
                )

        return {"classes": classes, "functions": functions}
    except Exception as e:
        return {"classes": [], "functions": []}


def build_structure(path):
    structure = {}
    try:
        items = os.listdir(path)
    except:
        return {}

    for item in items:
        # Pular pastas de infra e redundantes
        if item.startswith(".") or item in [
            "__pycache__",
            "venv",
            "node_modules",
            "kimi-dev-docker",
            "kimi_venv",
            "docs",
            "logs",
        ]:
            continue

        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            res = build_structure(full_path)
            if res:
                structure[item] = res
        elif item.endswith(".py") or item.endswith(".ts") or item.endswith(".tsx"):
            if os.path.isfile(full_path):
                if item.endswith(".py"):
                    structure[item] = get_class_function_info(full_path)
                else:
                    structure[item] = (
                        {}
                    )  # Por enquanto apenas metadata estrutural para TS/JS
        else:
            # Pular outros arquivos para manter o contexto limpo para o Llama 3b
            pass
    return structure


if __name__ == "__main__":
    root_path = "/app/luna_os_to_diagnose"
    print(f"🏗️ Refinando índice LUNA OS em {root_path}...")

    # Focar apenas em backend e frontend para o diagnóstico
    luna_structure = {}
    for folder in ["backend", "frontend"]:
        p = os.path.join(root_path, folder)
        if os.path.exists(p):
            luna_structure[folder] = build_structure(p)

    data = {"repo": "MCT/LUNA_OS", "base_commit": "latest", "structure": luna_structure}

    output_file = "/app/repo_structures/luna__luna-os.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(data, f)

    print(f"✅ Índice refinado gerado em: {output_file}")
