#!/usr/bin/env bash
# Откат на указанный тег образа (по умолчанию — из .current_tag, т. е. последний удачный).
#   IMAGE_TAG=<tag> deploy/scripts/rollback.sh
# Схему БД не откатывает.
set -euo pipefail
source "$(dirname "$0")/_compose.sh"

IMAGE_TAG="${IMAGE_TAG:-$(cat .current_tag 2>/dev/null || echo "")}"
: "${IMAGE_TAG:?нет тега для отката}"
export IMAGE_TAG

echo "Откат на ${IMAGE_TAG}"
compose up -d --remove-orphans
deploy/scripts/healthcheck.sh
echo "$IMAGE_TAG" > .current_tag
