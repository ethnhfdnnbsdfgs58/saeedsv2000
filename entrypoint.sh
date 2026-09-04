#!/bin/sh

echo "🚀 Generating configuration..."
cd /app

# تست xray
echo "Testing xray..."
which xray
xray version
xray x25519

python3 generate-config.py

echo "🔧 Starting Xray..."
exec /usr/bin/xray -config /etc/xray/config.json
