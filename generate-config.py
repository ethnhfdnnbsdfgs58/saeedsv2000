#!/usr/bin/env python3
import subprocess
import json
import uuid
import os

def main():
    user_uuid = str(uuid.uuid4())
    
    host = os.environ.get('RAILWAY_STATIC_URL', 'your-project.railway.app')
    host = host.replace('https://', '').replace('http://', '')
    
    config = {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "port": 443,
                "protocol": "vless",
                "settings": {
                    "clients": [{"id": user_uuid, "flow": "xtls-rprx-vision"}],
                    "decryption": "none"
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "tls",
                    "tlsSettings": {
                        "serverName": host,
                        "fingerprint": "chrome",
                        "alpn": ["h2", "http/1.1"]
                    }
                }
            }
        ],
        "outbounds": [{"protocol": "freedom", "tag": "direct"}]
    }
    
    with open('/etc/xray/config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    vless_link = f"vless://{user_uuid}@{host}:443?encryption=none&security=tls&sni={host}&fp=chrome&type=tcp&headerType=none#Railway-TCP"
    
    print(f"✅ UUID: {user_uuid}")
    print(f"✅ Host: {host}")
    print(f"✅ Link: {vless_link}")
    
    with open('/app/connection-link.txt', 'w') as f:
        f.write(vless_link)

if __name__ == "__main__":
    main()
