#!/usr/bin/env python3
import subprocess
import json
import uuid
import os

def generate_keys():
    try:
        result = subprocess.run(['xray', 'x25519'], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        
        print(f"🔍 xray output: {output}")
        
        private_key = ""
        public_key = ""
        
        for line in output.split('\n'):
            # فرمت جدید: PrivateKey: xxx
            if 'PrivateKey:' in line:
                private_key = line.split('PrivateKey:')[1].strip()
            # فرمت جدید: Password (PublicKey): xxx
            elif 'Password (PublicKey):' in line:
                public_key = line.split('Password (PublicKey):')[1].strip()
            # فرمت قدیمی: Private key: xxx
            elif 'Private key:' in line:
                private_key = line.split('Private key:')[1].strip()
            # فرمت قدیمی: Public key: xxx
            elif 'Public key:' in line:
                public_key = line.split('Public key:')[1].strip()
        
        if private_key and public_key:
            print(f"✅ Keys extracted - Private: {private_key[:10]}..., Public: {public_key[:10]}...")
            return private_key, public_key
        else:
            raise Exception(f"Keys not found. Private: {private_key}, Public: {public_key}")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return "", ""

def main():
    user_uuid = str(uuid.uuid4())
    private_key, public_key = generate_keys()
    short_id = uuid.uuid4().hex[:8]
    
    if not private_key or not public_key:
        print("❌ Failed to generate keys!")
        return
    
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
        print(f"✅ Private Key: {private_key}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
