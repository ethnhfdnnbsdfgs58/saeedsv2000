#!/usr/bin/env python3
import subprocess
import json
import uuid
import base64
import sys

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def generate_keys():
    # اجرای دستور xray برای تولید کلید
    output = run_command("xray x25519")
    lines = output.split('\n')
    private_key = ""
    public_key = ""
    for line in lines:
        if "Private key:" in line:
            private_key = line.split(":")[1].strip()
        elif "Public key:" in line:
            public_key = line.split(":")[1].strip()
    return private_key, public_key

def generate_short_id():
    # تولید short ID 8 کاراکتری
    return uuid.uuid4().hex[:8]

def main():
    # تولید UUID
    user_uuid = str(uuid.uuid4())
    
    # تولید کلیدهای Reality
    private_key, public_key = generate_keys()
    
    # تولید short ID
    short_id = generate_short_id()
    
    # خواندن config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # جایگزینی placeholderها
    config['inbounds'][0]['settings']['clients'][0]['id'] = user_uuid
    config['inbounds'][0]['streamSettings']['realitySettings']['privateKey'] = private_key
    config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'][0] = short_id
    
    # ذخیره config جدید
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # نمایش اطلاعات
    print("\n" + "="*50)
    print("🔑 اطلاعات تولید شده:")
    print("="*50)
    print(f"UUID: {user_uuid}")
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
    print(f"Short ID: {short_id}")
    print("="*50)
    
    # ذخیره در فایل برای استفاده بعدی
    with open('connection-info.txt', 'w') as f:
        f.write(f"UUID: {user_uuid}\n")
        f.write(f"Private Key: {private_key}\n")
        f.write(f"Public Key: {public_key}\n")
        f.write(f"Short ID: {short_id}\n")

if __name__ == "__main__":
    main()