#!/bin/bash
set -e
export DATA_DIR="${DATA_DIR:-/data}"
export PORT="${PORT:-8080}"
mkdir -p "$DATA_DIR"
[ -f "$DATA_DIR/sat_platform.db" ] || cp /app/sat_platform.db "$DATA_DIR/sat_platform.db"

if [ -z "$ADMIN_PASS" ]; then echo "OGOHLANTIRISH: ADMIN_PASS o'rnatilmagan, ustoz paneliga kirib bo'lmaydi!"; fi

gunicorn -b 127.0.0.1:5000 -w 2 --timeout 60 server:app &
streamlit run ustoz_app.py \
  --server.port 8501 --server.address 127.0.0.1 \
  --server.baseUrlPath ustoz --server.headless true \
  --browser.gatherUsageStats false &
caddy run --config /app/Caddyfile.internal --adapter caddyfile &

# birortasi o'lsa, konteyner to'xtaydi va platforma qayta ishga tushiradi
wait -n
exit 1
