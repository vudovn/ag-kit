#!/bin/bash
# Start Backend Script

echo "🚀 Starting LUNA OS Backend..."

cd /Users/franciscotaveira.ads/Documents/antigravity-kit/LUNA_OS/backend

# Activate venv
source venv/bin/activate

# Start uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
