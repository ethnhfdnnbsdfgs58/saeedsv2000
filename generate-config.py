#!/usr/bin/env python3
import subprocess
import json
import uuid
import os

def generate_keys():
    try:
        result = subprocess.run(['xray', 'x25519'], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        
        private_key = ""
        public_key = ""
        
        for line in output.split('\n'):
            if 'PrivateKey:' in line:
                private_key = line.split('PrivateKey:')[1].strip()
            elif 'Password (PublicKey):' in line:
                public_key = line.split('Password (PublicKey):')[1].strip()
            elif 'Private key:' in line:
                private_key = line.split('Private key:')[1].strip()
            elif 'Public key:' in line:
                public_key = line.split('Public key:')[1].strip()
        
        if private_key and public_key:
            return private_key, public_key
        else:
            raise Exception("Keys not found")
            
    except Exception as e:
        print(f"⚠️ Error generating keys: {e}")
        return "", ""

def main():
    user_uuid = str(uuid.uuid4())
    private_key, public_key = generate_keys()
    short_id = uuid.uuid4().hex[:8]
    
    print(f"🔑 Private Key: {private_key}")
    print(f"🔑 Public Key: {public_key}")
    
    # دریافت اطلاعات از Railway
    host = os.environ.get('RAILWAY_STATIC_URL', 'your-project.railway.app')
    host = host.replace('https://', '').replace('http://', '')
    
    # ساخت کانفیگ VLESS+WS+TLS
    config = {
        "log": {
            "loglevel": "warning"
        },
        "inbounds": [
            {
                "port": 443,
                "protocol": "vless",
                "settings": {
                    "clients": [
                        {
                            "id": user_uuid,
                            "flow": "xtls-rprx-vision"
                        }
                    ],
                    "decryption": "none"
                },
                "streamSettings": {
                    "network": "ws",
                    "security": "tls",
                    "tlsSettings": {
                        "serverName": host,
                        "fingerprint": "chrome",
                        "alpn": ["h2", "http/1.1"]
                    },
                    "wsSettings": {
                        "path": f"/ws/{user_uuid}",
                        "host": host
                    }
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "freedom",
                "tag": "direct"
            }
        ]
    }
    
    # ذخیره کانفیگ
    with open('/etc/xray/config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # ساخت لینک اتصال
    vless_link = f"vless://{user_uuid}@{host}:443?encryption=none&security=tls&sni={host}&fp=chrome&type=ws&host={host}&path=/ws/{user_uuid}#Railway-WS"
    
    print(f"✅ UUID: {user_uuid}")
    print(f"✅ Public Key: {public_key}")
    print(f"✅ Short ID: {short_id}")
    print(f"✅ Host: {host}")
    print(f"✅ Link: {vless_link}")
    
    # ذخیره لینک در فایل
    with open('/app/connection-link.txt', 'w') as f:
        f.write(vless_link)
        f.write("\n\n")
        f.write(f"UUID: {user_uuid}\n")
        f.write(f"Public Key: {public_key}\n")
        f.write(f"Short ID: {short_id}\n")
        f.write(f"Host: {host}\n")

if __name__ == "__main__":
    main()
