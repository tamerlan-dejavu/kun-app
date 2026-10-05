# KUN

Сервис сборов небольших компаний (3–6 человек) для молодёжи Алматы.
Этап 1 — веб MVP (PWA), бэкенд с API, админка модерации, Telegram-бот уведомлений.

## Структура

| Папка | Что внутри |
|---|---|
| `backend/` | Django 5 + DRF, Channels (WebSocket), Celery, PostGIS |
| `web/` | Next.js (TypeScript), Tailwind, TanStack Query, PWA |
| `deploy/` | Docker Compose, Nginx, скрипты выкладки и бэкапов |
| `mobile/` | Этап 3: React Native (Expo) |
| `.github/` | CI/CD (GitHub Actions) |

## Запуск локально

```bash
cp .env.example .env
make up            # миграции и collectstatic выполняются при старте api
make superuser     # вход в /admin
```

Без make (Windows):
`docker compose --env-file .env -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml up --build`

- сайт: http://localhost
- API и Swagger: http://localhost/api/v1/docs/
- админка: http://localhost/admin/
- Postgres: localhost:**5433** (порт в `DB_HOST_PORT`), база `kun`, пользователь/пароль `kun`/`kun` (DataGrip, psql)

Демо-данные (пользователи, сборы, чат, оценки, жалобы): `make seed`.
Чистая БД с нуля: `make reset-db` (удаляет только тома проекта `kun-app`).

Попробовать API руками, пока нет входа по телефону (только dev):
http://localhost/api/v1/auth/dev/login/ → `+77000000001` / `kun-demo` (модератор — `+77000000000`).
После входа открывается браузерный API DRF: лента `/api/v1/gatherings`, сбор `/api/v1/gatherings/1`,
кнопки POST для join/leave. Swagger: http://localhost/api/v1/docs/

## Модель данных

| Приложение | Таблицы |
|---|---|
| accounts | `user` (вход по телефону, профиль, надёжность), `authcode` (хэши кодов SMS), `usersession` |
| universities | `university` — справочник для необязательного поля профиля |
| catalog | `category` (категории сборов), `interest` (интересы профиля) |
| gatherings | `gathering`, `participation` (left_at IS NULL — в сборе), `attendance` («Я пришёл»), `rating` |
| chat | `message` (участников и системные) |
| notifications | `notificationsettings`, `pushsubscription`, `telegramlink` |
| moderation | `report`, `block`, `usersanction`, `bannedword`, `moderationlog` (UPDATE/DELETE запрещены триггером) |

Правила из ТЗ, которые проверяет сама БД: 3–6 мест, один активный участник и один создатель на сбор,
«Я пришёл» один раз, нельзя оценить или заблокировать себя, жалоба ровно на одну цель,
у отменённого сбора есть дата отмены, у паузы — дата окончания. У таблиц и колонок есть комментарии.

В dev SMS не отправляются — код входа пишется в лог сервиса `api`.

Перед PR: `make check-backend` (то же, что CI) и `make openapi`, если менялось API
(коммитим `web/src/lib/api/schema.d.ts`).

## Ветки

```
feature/<задача> ──PR──► develop ──PR──► main ──тег vX.Y.Z──► production
                            │
                            └──merge──► staging (автоматически)
hotfix/<что> ──PR──► main (и потом в develop)
```

| Ветка | Откуда | Куда | Назначение |
|---|---|---|---|
| `main` | — | — | то, что в production; прямые пуши запрещены |
| `develop` | `main` | `main` | интеграция; всё отсюда сразу на staging |
| `feature/*` | `develop` | `develop` | одна задача, например `feature/auth-phone` |
| `release/*` | `develop` | `main` + `develop` | при необходимости стабилизировать релиз |
| `hotfix/*` | `main` | `main` + `develop` | срочная починка production |

```bash
git switch develop && git pull
git switch -c feature/auth-phone
# ...коммиты...
git push -u origin feature/auth-phone   # и открыть PR в develop
```

## CI/CD (GitHub Actions)

| Событие | Workflow | Что происходит |
|---|---|---|
| PR в `develop` или `main` | `ci.yml` | backend: ruff, миграции, pytest, OpenAPI; web: типы из OpenAPI актуальны, lint, typecheck, build |
| PR в `main` | `ci.yml` → `branch-policy` | только из `develop`, `release/*`, `hotfix/*` |
| merge в `develop` | `deploy-staging.yml` | CI → образы `api` и `web` в GHCR (тег = SHA) → выкладка на staging |
| тег `vX.Y.Z` на коммите из `main` | `deploy-production.yml` | проверка, что тег в `main` → CI → образы (тег = версия) → **ручное подтверждение** → production |

Пока в Environment не задан `DEPLOY_HOST`, выкладка собирает и пушит образы, но SSH-шаги пропускает.

Релиз:

```bash
# PR develop -> main смёржен
git switch main && git pull
git tag v1.0.0 && git push origin v1.0.0
```

### Защита веток (Settings → Branches → Add rule), один раз

- `main` и `develop`: Require a pull request before merging; Require status checks to pass —
  `backend`, `web` (для `main` ещё `branch-policy`); Do not allow bypassing; запрет force push.
- `main`: Require approvals — 1.

## Выкладка

### Один раз на сервере (staging и production)

1. Docker с плагином compose; пользователь деплоя в группе `docker`.
2. `mkdir /opt/kun` и `/opt/kun/.env` по образцу `.env.example`:
   `DJANGO_SETTINGS_MODULE=config.settings.prod`, `REGISTRY=ghcr.io/tamerlan-dejavu/kun-app`,
   `DOMAIN`, `ALLOWED_HOSTS`, секреты.
3. TLS: первичный выпуск сертификата и блок `listen 443` в `deploy/nginx/conf.d/kun.conf` — TODO.
4. Cron для `deploy/scripts/backup.sh` (пример в самом скрипте).

### В GitHub (Settings → Environments → staging / production)

- secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`
- vars: `SITE_URL`, `VAPID_PUBLIC_KEY`, `SENTRY_DSN_WEB` (вшиваются в сборку web)
- production: включить Required reviewers

Ручной откат на сервере: `IMAGE_TAG=<тег> deploy/scripts/rollback.sh` (схему БД не откатывает).
