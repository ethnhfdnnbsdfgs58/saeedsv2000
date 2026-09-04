FROM teddysun/xray:latest

WORKDIR /app

# کپی همه فایل‌ها به مسیر درست
COPY config.json /etc/xray/config.json
COPY generate-config.py /app/generate-config.py
COPY entrypoint.sh /app/entrypoint.sh

RUN apk add --no-cache python3 py3-pip bash curl jq

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
