#!/bin/sh

echo "🚀 Generating configuration..."
python3 /app/generate-config.py

echo "🔧 Starting Xray..."
exec /usr/bin/xray -config /etc/xray/config.json