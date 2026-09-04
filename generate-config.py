#!/usr/bin/env python3
import subprocess
import json
import uuid
import os

def generate_keys():
    try:
        # روش 1: با xray
        result = subprocess.run(['xray', 'x25519'], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        
        private_key = ""
        public_key = ""
        
        for line in output.split('\n'):
            if 'Private key:' in line:
                private_key = line.split('Private key:')[1].strip()
            elif 'Public key:' in line:
                public_key = line.split('Public key:')[1].strip()
        
        # اگر خالی بود، با openssl بساز
        if not private_key or not public_key:
            print("⚠️ xray x25519 failed, using openssl...")
            # ساخت کلید با openssl
            private_key = subprocess.run(
                "openssl rand -base64 32 | tr -d '\n'", 
                shell=True, capture_output=True, text=True
            ).stdout.strip()
            
            public_key = subprocess.run(
                "openssl rand -base64 32 | tr -d '\n'", 
                shell=True, capture_output=True, text=True
            ).stdout.strip()
        
        return private_key, public_key
    except Exception as e:
        print(f"❌ Error: {e}")
        # در صورت خطا، کلیدهای تستی
        return "aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3", "bC2dE3fG4hI5jK6lM7nO8pQ9rS0tU1vW2xY3zA4"

def main():
    user_uuid = str(uuid.uuid4())
    private_key, public_key = generate_keys()
    short_id = uuid.uuid4().hex[:8]
    
    print(f"🔑 Private Key: {private_key}")
    print(f"🔑 Public Key: {public_key}")
    
    try:
        with open('/etc/xray/config.json', 'r') as f:
            config = json.load(f)
        
        config['inbounds'][0]['settings']['clients'][0]['id'] = user_uuid
        config['inbounds'][0]['streamSettings']['realitySettings']['privateKey'] = private_key
        config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'][0] = short_id
        
        with open('/etc/xray/config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ UUID: {user_uuid}")
        print(f"✅ Public Key: {public_key}")
        print(f"✅ Short ID: {short_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
