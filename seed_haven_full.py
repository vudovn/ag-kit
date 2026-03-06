import json
import requests
import uuid
import os

API_URL = "http://localhost:8000/api/knowledge/"
KNOWLEDGE_DIR = "/Users/franciscotaveira.ads/Local_Dev/Mothership_Core/command-tower/agents/haven-receptionist/knowledge"


def push_item(category, key, data):
    payload = {"category": category, "key": key, "data": data}
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Success: {category} -> {key}")
        else:
            print(f"❌ Error {response.status_code} on {key}: {response.text}")
    except Exception as e:
        print(f"💥 Failed to connect to API for {key}: {e}")


def seed_services():
    with open(os.path.join(KNOWLEDGE_DIR, "services.json"), "r") as f:
        services = json.load(f)
        for s in services:
            push_item("services", s["id"], s)


def seed_professionals():
    with open(os.path.join(KNOWLEDGE_DIR, "professionals.json"), "r") as f:
        profs = json.load(f)
        for p in profs:
            push_item("professionals", p["id"], p)


def seed_logic():
    with open(os.path.join(KNOWLEDGE_DIR, "behavioral_logic.json"), "r") as f:
        logic = json.load(f)
        for key, value in logic.items():
            push_item("behavioral_logic", key, value)


def seed_others():
    files = [
        "business.json",
        "coupons.json",
        "packages.json",
        "upsells.json",
        "rules.json",
    ]
    for filename in files:
        category = filename.split(".")[0]
        with open(os.path.join(KNOWLEDGE_DIR, filename), "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                for i, item in enumerate(data):
                    key = item.get("id") or item.get("coupon") or f"{category}_{i}"
                    push_item(category, key, item)
            else:
                for key, value in data.items():
                    push_item(category, key, value)


if __name__ == "__main__":
    print("🚀 Starting full Haven Protocol ingestion into LUNA Brain...")
    seed_services()
    seed_professionals()
    seed_logic()
    seed_others()
    print("🏁 Ingestion complete!")
