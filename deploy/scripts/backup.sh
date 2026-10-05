#!/usr/bin/env bash
# Ежедневный бэкап БД, хранение 14 дней. Cron на сервере:
#   0 3 * * * /opt/kun/deploy/scripts/backup.sh >> /opt/kun/backups/backup.log 2>&1
set -euo pipefail
source "$(dirname "$0")/_compose.sh"

BACKUP_DIR="${BACKUP_DIR:-$(pwd)/backups}"
mkdir -p "$BACKUP_DIR"

FILE="$BACKUP_DIR/kun-$(date +%F).dump"
compose exec -T db pg_dump -U "${POSTGRES_USER:-kun}" -Fc "${POSTGRES_DB:-kun}" > "$FILE"
find "$BACKUP_DIR" -name 'kun-*.dump' -mtime +14 -delete
echo "Бэкап: $FILE"
# TODO: копия во внешнее хранилище в РК
