"""Журнал модерации неизменяем на уровне БД (раздел 4 ТЗ): UPDATE и DELETE запрещены триггером.

Так запрет действует и для запросов мимо Django — из DataGrip, psql, скриптов.
TRUNCATE (manage.py flush в тестах/dev) триггер не блокирует — это осознанно.
"""

from django.db import migrations

FORWARD = """
CREATE OR REPLACE FUNCTION moderation_log_immutable() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'moderation_moderationlog is append-only: % is not allowed', TG_OP;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER moderation_log_no_update_delete
    BEFORE UPDATE OR DELETE ON moderation_moderationlog
    FOR EACH ROW EXECUTE FUNCTION moderation_log_immutable();
"""

BACKWARD = """
DROP TRIGGER IF EXISTS moderation_log_no_update_delete ON moderation_moderationlog;
DROP FUNCTION IF EXISTS moderation_log_immutable();
"""


class Migration(migrations.Migration):
    dependencies = [("moderation", "0001_initial")]

    operations = [migrations.RunSQL(FORWARD, BACKWARD)]
