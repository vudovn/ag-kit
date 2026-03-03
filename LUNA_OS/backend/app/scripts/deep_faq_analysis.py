#!/usr/bin/env python3
"""
🌙🔍 LUNA OS — DEEP FAQ & SENTIMENT ANALYSIS
Análise profunda de FAQs e sentimento nas conversas
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

# Paths
EXTRACTIONS_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs/extractions")
OUTPUT_DIR = Path("/Users/franciscotaveira.ads/LUNA OS/logs/analytics")

# Load latest extraction
files = list(EXTRACTIONS_DIR.glob("whatsapp_conversations_*.json"))
latest_file = sorted(files)[-1]
print(f"📂 Loading: {latest_file.name}")

with open(latest_file, 'r') as f:
    data = json.load(f)

conversations = data.get("conversations", [])
print(f"📊 Analyzing {len(conversations)} conversations...")
print()

# ============================================================================
# ANALISAR PRIMEIRAS E ÚLTIMAS MENSAGENS EM DETALHE
# ============================================================================
print("=" * 80)
print("🔍 ANÁLISE DE CONTEÚDO DAS MENSAGENS")
print("=" * 80)

# Collect all first and last contents
first_messages = []
last_messages = []

for conv in conversations:
    if conv.get("first_content"):
        first_messages.append(conv["first_content"])
    if conv.get("last_content"):
        last_messages.append(conv["last_content"])

# Print samples
print("\n📋 EXEMPLOS DE PRIMEIRAS MENSAGENS (clientes iniciando):\n")
for i, msg in enumerate(first_messages[:15], 1):
    print(f"{i}. {msg}")

print("\n📋 EXEMPLOS DE ÚLTIMAS MENSAGENS:\n")
for i, msg in enumerate(last_messages[:15], 1):
    print(f"{i}. {msg}")

# ============================================================================
# DETECÇÃO DE TÓPICOS COM N-GRAMS
# ============================================================================
print()
print("=" * 80)
print("📊 ANÁLISE DE N-GRAMS (palavras e frases mais comuns)")
print("=" * 80)

# Combine all text
all_text = " ".join(first_messages + last_messages).lower()

# Remove special chars
all_text = re.sub(r'[^\w\sáàãâéêíóôõúç]', ' ', all_text)

# Word frequencies
words = all_text.split()
word_counts = Counter(words)

# Filter common words
stop_words = {'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'em', 'no', 'na', 
              'para', 'com', 'por', 'que', 'qual', 'quais', 'como', 'quando', 'onde',
              'me', 'te', 'se', 'nos', 'lhe', 'lhes', 'é', 'eh', 'ser', 'foi', 'foram',
              'tem', 'ter', 'tinha', 'tive', 'teve', 'quero', 'queria', 'gostaria',
              'ola', 'olá', 'oi', 'bom', 'dia', 'tarde', 'noite', 'tudo', 'bem', 'nao', 'não', 'sim'}

filtered_words = [(w, c) for w, c in word_counts.items() if w not in stop_words and len(w) > 2]
top_words = sorted(filtered_words, key=lambda x: x[1], reverse=True)[:30]

print("\n📋 PALAVRAS MAIS FREQUENTES:\n")
for word, count in top_words:
    print(f"   • {word}: {count}")

# Bigrams (pairs of words)
bigrams = zip(words[:-1], words[1:])
bigram_counts = Counter([f"{w1} {w2}" for w1, w2 in bigrams if w1 not in stop_words or w2 not in stop_words])
top_bigrams = bigram_counts.most_common(20)

print("\n📋 FRASES DE 2 PALAVRAS MAIS COMUNS:\n")
for phrase, count in top_bigrams:
    if count > 2:
        print(f"   • \"{phrase}\": {count}")

# ============================================================================
# DETECÇÃO DE INTENÇÕES ESPECÍFICAS
# ============================================================================
print()
print("=" * 80)
print("🎯 DETECÇÃO DE INTENÇÕES")
print("=" * 80)

intention_patterns = {
    "AGENDAMENTO": [
        r"agendar", r"agenda", r"marcar", r"reservar", r"horário", r"horario",
        r"disponível", r"disponivel", r"vaga", r"encaixar"
    ],
    "PRECO": [
        r"valor", r"preço", r"preco", r"quanto", r"custa", r"paga", r"pagar",
        r"promoc", r"desconto", r"barato", r"caro", r"tabela"
    ],
    "SERVICO": [
        r"unha", "unhas", "cabelo", "escova", "penteado", "tratamento",
        r"sobrancelh", r"cílio", r"cilios", r"gel", r"manicure", r"pedicure",
        r"esmalte", r"maquiagem", r"limpeza", r"hidrata", r"corte", r"pé", r"mao"
    ],
    "LOCALIZACAO": [
        r"onde", r"fica", r"endereço", r"endereco", r"local", r"rua", r"avenida",
        r"bairro", r"cidade", r"próximo", r"proximo", r"chegar", r"estacionamento"
    ],
    "INFORMACAO": [
        r"funciona", r"horário", r"horario", r"aberto", r"fechado", r"feira",
        r"sábado", r"domingo", r"ligar", r"telefone", r"zap", r"whatsapp"
    ],
    "RECLAMACAO": [
        r"demora", r"demorou", r"atraso", r"atrasou", r"ruim", r"péssimo",
        r"problema", r"erro", r"reclamar", r"insatisfeito", r"não gostei", "nao gostei"
    ],
    "ELOGIO": [
        r"amei", r"adoro", r"perfeito", r"maravilha", r"lindo", r"incrível",
        r"excelente", r"recomendo", r"satisfeita", r"gostei", r"amei"
    ]
}

intention_counts = defaultdict(int)
intention_examples = defaultdict(list)

for conv in conversations:
    text = (conv.get("first_content", "") or "" + " " + conv.get("last_content", "") or "").lower()
    
    for intention, patterns in intention_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                intention_counts[intention] += 1
                if len(intention_examples[intention]) < 3:
                    example = (conv.get("first_content", "") or "")[:60]
                    intention_examples[intention].append(example)
                break

print("\n📋 INTENÇÕES DETECTADAS:\n")
print(f"{'Intenção':<20} {'Ocorrências':<15}")
print("-" * 35)
for intention, count in sorted(intention_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{intention:<20} {count:<15}")

# ============================================================================
# ANALISE DE SENTIMENTO SIMPLIFICADA
# ============================================================================
print()
print("=" * 80)
print("😊 ANÁLISE DE SENTIMENTO")
print("=" * 80)

positive_words = ['amei', 'adoro', 'perfeito', 'maravilha', 'lindo', 'incrível', 
                  'excelente', 'recomendo', 'satisfeita', 'gostei', 'obrigada', 
                  'obrigado', 'top', 'show', 'demais', '❤️', '💕', '🥰', '😍']
negative_words = ['ruim', 'péssimo', 'odiei', 'insatisfeita', 'decepção', 
                  'decepcao', 'não gostei', 'nao gostei', 'nunca mais', 'jamais',
                  'problema', 'erro', 'demora', 'atraso']

positive_count = 0
negative_count = 0
neutral_count = 0

for conv in conversations:
    text = (conv.get("first_content", "") or "" + " " + conv.get("last_content", "") or "").lower()
    
    has_positive = any(word in text for word in positive_words)
    has_negative = any(word in text for word in negative_words)
    
    if has_positive and not has_negative:
        positive_count += 1
    elif has_negative and not has_positive:
        negative_count += 1
    else:
        neutral_count += 1

total = positive_count + negative_count + neutral_count

print(f"\n📊 DISTRIBUIÇÃO DE SENTIMENTO:\n")
print(f"   • Positivo: {positive_count} ({positive_count/total*100:.1f}%)")
print(f"   • Negativo: {negative_count} ({negative_count/total*100:.1f}%)")
print(f"   • Neutro: {neutral_count} ({neutral_count/total*100:.1f}%)")

# ============================================================================
# SALVAR RESULTADOS
# ============================================================================
report = {
    "generated_at": datetime.now().isoformat(),
    "top_words": [{"word": w, "count": c} for w, c in top_words],
    "top_bigrams": [{"phrase": p, "count": c} for p, c in top_bigrams if c > 2],
    "intentions": dict(intention_counts),
    "intention_examples": dict(intention_examples),
    "sentiment": {
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count
    },
    "message_samples": {
        "first_messages": first_messages[:20],
        "last_messages": last_messages[:20]
    }
}

with open(OUTPUT_DIR / "deep_faq_sentiment_analysis.json", 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved to: {OUTPUT_DIR / 'deep_faq_sentiment_analysis.json'}")
print()
print("=" * 80)
print("✅ ANÁLISE PROFUNDA CONCLUÍDA!")
print("=" * 80)
