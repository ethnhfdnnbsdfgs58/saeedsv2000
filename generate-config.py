#!/usr/bin/env python3
import subprocess
import json
import uuid
import re

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def generate_keys():
    output = run_command("xray x25519")
    # روش بهتر برای استخراج
    private_key = ""
    public_key = ""
    for line in output.split('\n'):
        if "Private key:" in line:
            private_key = line.split("Private key:")[1].strip()
        elif "Public key:" in line:
            public_key = line.split("Public key:")[1].strip()
    return private_key, public_key

def main():
    user_uuid = str(uuid.uuid4())
    private_key, public_key = generate_keys()
    short_id = uuid.uuid4().hex[:8]
    
    # چاپ برای دیباگ
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
    
    with open('/etc/xray/config.json', 'r') as f:
        config = json.load(f)
    
    config['inbounds'][0]['settings']['clients'][0]['id'] = user_uuid
    config['inbounds'][0]['streamSettings']['realitySettings']['privateKey'] = private_key
    config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'][0] = short_id
    
    with open('/etc/xray/config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"UUID: {user_uuid}")
    print(f"Public Key: {public_key}")
    print(f"Short ID: {short_id}")

if __name__ == "__main__":
    main()
