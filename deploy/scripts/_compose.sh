#!/usr/bin/env bash
# Общее для скриптов на сервере. Подключается через `source`.
# Скрипты запускаются из корня (/opt/kun), где лежат .env и deploy/.

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

if [ ! -f .env ]; then
  echo ".env не найден в $(pwd)" >&2
  exit 1
fi

# DOMAIN, REGISTRY и др. — для скриптов; compose сам читает .env через --env-file
set -a
# shellcheck disable=SC1091
source .env
set +a

compose() {
  docker compose --env-file .env -f deploy/docker-compose.yml -f deploy/docker-compose.prod.yml "$@"
}
