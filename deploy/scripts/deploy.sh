#!/usr/bin/env bash
# Выкладка на сервере: pull -> migrate -> collectstatic -> up -d -> health-check.
# При неудачном health-check откат на предыдущий тег.
#   IMAGE_TAG=<tag> deploy/scripts/deploy.sh
set -euo pipefail
source "$(dirname "$0")/_compose.sh"

: "${IMAGE_TAG:?IMAGE_TAG не задан}"
: "${REGISTRY:?REGISTRY не задан в .env}"
export IMAGE_TAG

PREV_TAG=$(cat .current_tag 2>/dev/null || echo "")
echo "Выкладка ${IMAGE_TAG} (предыдущий: ${PREV_TAG:-нет})"

compose pull

# Миграции до переключения: новый код не стартует со старой схемой.
# Миграции должны быть обратно совместимы — откат меняет только образы, не схему БД.
compose run --rm api python manage.py migrate --noinput
compose run --rm api python manage.py collectstatic --noinput

compose up -d --remove-orphans

if ! deploy/scripts/healthcheck.sh; then
  echo "Health-check не прошёл" >&2
  if [ -n "$PREV_TAG" ]; then
    IMAGE_TAG="$PREV_TAG" deploy/scripts/rollback.sh
  fi
  exit 1
fi

echo "$IMAGE_TAG" > .current_tag
docker image prune -f > /dev/null
echo "Готово: ${IMAGE_TAG}"
