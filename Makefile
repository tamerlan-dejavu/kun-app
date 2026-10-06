# --env-file .env: корневой .env для подстановки ${...} в compose (иначе compose ищет deploy/.env)
COMPOSE = docker compose --env-file .env -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f api ws worker beat

migrate:
	$(COMPOSE) run --rm api python manage.py migrate

makemigrations:
	$(COMPOSE) run --rm api python manage.py makemigrations

superuser:
	$(COMPOSE) run --rm api python manage.py createsuperuser

# Демо-данные для DataGrip и админки (только dev)
seed:
	$(COMPOSE) run --rm api python manage.py seed_demo

# Ещё сборы на неделю и история встреч — для «Для тебя»
seed-more:
	$(COMPOSE) run --rm api python manage.py seed_demo --more

# Пересоздать локальную БД с нуля: удаляет тома проекта kun-app (БД и статику), не трогая другие проекты
reset-db:
	$(COMPOSE) down -v
	$(COMPOSE) up -d --wait db redis
	$(COMPOSE) run --rm api python manage.py migrate

test-backend:
	$(COMPOSE) run --rm api pytest

# То же, что CI делает для бэкенда
check-backend:
	$(COMPOSE) run --rm api sh -c "ruff check . && ruff format --check . && python manage.py makemigrations --check --dry-run && pytest"

# Схема OpenAPI -> типы для фронта (коммитить web/src/lib/api/schema.d.ts)
openapi:
	$(COMPOSE) run --rm api python manage.py spectacular --file openapi.yaml
	cd web && npm run gen:api

.PHONY: up down logs migrate makemigrations superuser seed seed-more reset-db test-backend check-backend openapi
