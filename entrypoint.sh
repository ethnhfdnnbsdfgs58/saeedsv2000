#!/bin/sh

echo "🚀 Generating configuration..."
cd /app
python3 generate-config.py

echo "🔧 Starting Xray..."
exec /usr/bin/xray -config /etc/xray/config.json
