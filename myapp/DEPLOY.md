# SAT Platform — Deploy

Bitta Docker image: `/` = o'quvchi (Flask), `/ustoz/` = ustoz paneli (Streamlit).
Ma'lumotlar `/data/sat_platform.db` da (birinchi ishga tushishda zipdagi baza nusxalanadi).

## A) Hetzner (asosiy)
1. Hetzner Cloud: Ubuntu 24.04, CX22 yetarli. IP manzilni oling.
2. Domen DNS: `A  @  -> IP` va `A  www -> IP`
3. Serverga: `ssh root@IP`, so'ng loyihani yuklang: `scp -r myapp root@IP:/opt/sat`
4. `cd /opt/sat && ./deploy_hetzner.sh`
5. `cp .env.example .env && nano .env` (DOMAIN va ADMIN_PASS ni to'ldiring)
6. `docker compose up -d --build` — HTTPS avtomatik (Caddy / Let's Encrypt).
Yangilash: fayllarni almashtirib `docker compose up -d --build`.
Zaxira: `./data/sat_platform.db` ni nusxalab qo'ying.

## B) Render (hozircha)
1. Loyihani GitHub'ga push qiling.
2. Render > New > Blueprint > repo tanlang (render.yaml avtomatik o'qiladi).
3. Environment: `ADMIN_PASS` ni kiriting.
4. Domen: Render > Settings > Custom Domains.
Eslatma: bepul rejada disk yo'q — baza har deployda yo'qoladi. `render.yaml` da `starter` + 1GB disk bor.

## Lokal
`python main.py` (avvalgidek ishlaydi; `ADMIN_PASS=... python main.py` bilan ustoz paneliga kirasiz).
