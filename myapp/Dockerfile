FROM caddy:2 AS caddy

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY --from=caddy /usr/bin/caddy /tmp/caddy
RUN cp /tmp/caddy /usr/local/bin/caddy && rm /tmp/caddy && chmod +x /usr/local/bin/caddy
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DATA_DIR=/data PORT=8080
EXPOSE 8080
CMD ["./start.sh"]
