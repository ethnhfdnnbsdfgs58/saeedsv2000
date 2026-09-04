#!/bin/sh

echo "🚀 Generating configuration..."
python3 generate-config.py  # ← مسیر رو عوض کن (بدون /app)

echo "🔧 Starting Xray..."
exec /usr/bin/xray -config /etc/xray/config.json
