FROM teddysun/xray:latest

WORKDIR /app

# کپی فایل‌های مورد نیاز
COPY config.json /etc/xray/config.json
COPY entrypoint.sh /entrypoint.sh

# نصب ابزارهای مورد نیاز برای اسکریپت
RUN apk add --no-cache python3 py3-pip bash curl jq

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]