#!/bin/bash
# Yangi Hetzner Ubuntu serverda (root sifatida) bir marta ishga tushiring
set -e
apt-get update && apt-get install -y ca-certificates curl ufw
curl -fsSL https://get.docker.com | sh
ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw --force enable
echo "Docker o'rnatildi. Endi loyihani /opt/sat ga yuklab: cp .env.example .env, tahrirlang, so'ng: docker compose up -d --build"
