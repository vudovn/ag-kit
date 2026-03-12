#!/bin/bash
echo "=== LUNA OS 100x RECOVERY === "
cd "/Users/franciscotaveira.ads/LUNA OS"
docker-compose down -v
rm -rf frontend/.next
docker-compose up --build -d
echo "Checking logs for 'use client' errors..."
sleep 15
docker-compose logs luna-frontend | grep -i "use client" || echo "✅ No client component errors detected."
