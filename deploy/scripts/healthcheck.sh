#!/usr/bin/env bash
# Проверка, что api (с БД и Redis) и web отвечают. Ходим внутрь контейнеров, мимо nginx и TLS:
# Host = $DOMAIN (есть в ALLOWED_HOSTS), X-Forwarded-Proto: https (иначе prod редиректит на HTTPS).
set -euo pipefail
source "$(dirname "$0")/_compose.sh"

: "${DOMAIN:?DOMAIN не задан в .env}"

check_api() {
  compose exec -T api python -c "
import urllib.request as u
req = u.Request('http://127.0.0.1:8000/api/v1/health/',
                headers={'Host': '${DOMAIN}', 'X-Forwarded-Proto': 'https'})
u.urlopen(req, timeout=5)
" > /dev/null 2>&1
}

check_web() {
  compose exec -T web wget -q -O /dev/null http://127.0.0.1:3000/ > /dev/null 2>&1
}

for i in $(seq 1 20); do
  if check_api && check_web; then
    echo "health-check: ok"
    exit 0
  fi
  echo "health-check: попытка ${i}/20..."
  sleep 3
done

echo "health-check: FAIL" >&2
compose ps >&2
exit 1
