FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# GeoDjango (PostGIS) и Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
        gdal-bin libgdal-dev libgeos-dev libproj-dev \
        libjpeg62-turbo-dev zlib1g-dev libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала только зависимости из pyproject.toml — слой кэшируется, пока они не меняются.
# INSTALL_DEV=1 (dev-compose) добавляет pytest, ruff и т. п.
ARG INSTALL_DEV=0
COPY pyproject.toml ./
RUN python -c "import tomllib; p = tomllib.load(open('pyproject.toml', 'rb'))['project']; \
deps = p['dependencies'] + (p['optional-dependencies']['dev'] if '$INSTALL_DEV' == '1' else []); \
open('/tmp/requirements.txt', 'w').write('\n'.join(deps))" \
    && pip install -r /tmp/requirements.txt

COPY . .

# Не root. staticfiles создаём заранее: именованный том static наследует владельца.
RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app
USER app

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000", "-w", "3"]
