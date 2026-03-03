import os
import re
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv("/Users/franciscotaveira.ads/LUNA OS/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Erro: SUPABASE_URL ou SUPABASE_KEY não configurados no .env")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

PROTOCOL_PATH = "/Users/franciscotaveira.ads/Documents/antigravity-kit/PROTOCOLO-HAVEN-SECRETARIA.md"


def parse_protocol(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Dividir por seções nível 2 (##) ou nível 3 (###) que representam tópicos significativos
    # Vamos focar em ### para granularidade, mas capturar o título da seção ##
    sections = re.split(r"\n(#{1,3}\s+)", content)

    items = []
    current_major_section = "Geral"

    # O split gera [lixo_inicial, # , titulo, conteúdo, #, titulo, conteúdo...]
    for i in range(1, len(sections), 2):
        prefix = sections[i].strip()
        header_and_body = sections[i + 1]

        lines = header_and_body.split("\n", 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        if not body:
            continue

        # Determinar categoria baseado no título ou posição
        category = "business"
        if prefix == "##":
            current_major_section = title
            # Mapeamento básico por palavras-chave
            if any(
                k in title.lower()
                for k in [
                    "serviço",
                    "preço",
                    "valor",
                    "pacote",
                    "gel",
                    "unha",
                    "cabelo",
                ]
            ):
                category = "services"
            elif any(
                k in title.lower()
                for k in ["protocolo", "fluxo", "como", "erro", "atendimento"]
            ):
                category = "faq"
        else:  # ###
            # Subseções herdam a lógica do título maior ou do título da subseção
            if any(
                k in title.lower()
                for k in [
                    "serviço",
                    "preço",
                    "valor",
                    "pacote",
                    "gel",
                    "unha",
                    "cabelo",
                ]
            ):
                category = "services"
            elif any(
                k in title.lower()
                for k in [
                    "protocolo",
                    "fluxo",
                    "como",
                    "erro",
                    "atendimento",
                    "passo",
                    "exemplo",
                ]
            ):
                category = "faq"
            elif any(k in title.lower() for k in ["postura", "secretária", "funções"]):
                category = "business"

        items.append(
            {
                "id": str(uuid.uuid4()),
                "category": category,
                "key": (
                    f"{current_major_section}: {title}" if prefix == "###" else title
                ),
                "data": {"content": body},
            }
        )

    return items


def ingest():
    print(f"📖 Lendo protocolo em: {PROTOCOL_PATH}")
    items = parse_protocol(PROTOCOL_PATH)
    print(f"✅ Encontrados {len(items)} itens para ingestão.")

    for item in items:
        try:
            # Upsert baseado em key e category (se a tabela tiver essa constraint)
            # Como não sabemos a constraint exata, vamos tentar inserir ou atualizar
            # A API da Luna sugere upsert por key,category
            res = (
                supabase.table("knowledge_base")
                .upsert(item, on_conflict="key,category")
                .execute()
            )
            print(f"✔ Ingerido: {item['key']} [{item['category']}]")
        except Exception as e:
            print(f"❌ Erro ao ingerir {item['key']}: {str(e)}")


if __name__ == "__main__":
    ingest()
