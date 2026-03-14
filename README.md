# Django Storefront (Practice Project)

This repository is a Django monolith that mixes a learning sandbox (`ground`) with a functional e‑commerce API (`store`), plus custom user accounts (`core`) and tagging/likes using generic relations (`tags`, `likes`). It includes DRF endpoints, JWT auth via Djoser, admin customizations, async tasks with Celery, caching, and basic tests.

## Key Features
- REST API for products, collections, carts, orders, reviews, and product images.
- Custom user model and JWT authentication (Djoser + SimpleJWT).
- Django admin enhancements (filters, inline edits, actions, image previews).
- Celery tasks + beat scheduling.
- Redis-backed caching.
- pytest + DRF tests and a Locust load test script.

## Tech Stack
- Django, Django REST Framework
- Djoser + SimpleJWT
- PostgreSQL (dev settings)
- Redis (cache + Celery broker)
- Celery, django-redis
- pytest, model-bakery, Locust

## Project Structure (High Level)
- `front/` — Django project settings and entrypoints (dev/prod split).
- `store/` — E‑commerce domain models + API endpoints.
- `core/` — Custom user model and base homepage.
- `ground/` — Sandbox/demo app for ORM, caching, and Celery examples.
- `tags/`, `likes/` — Generic relations for tagging and likes.
- `locustfiles/` — Load testing scripts.

## Setup (Local)
1. Create and activate a virtualenv.
2. Install dependencies (no lockfile provided; inferred list):
   ```bash
   pip install django djangorestframework django-filter django-cors-headers djoser \
     djangorestframework-simplejwt django-debug-toolbar django-silk whitenoise \
     celery redis django-redis requests pytest pytest-django model-bakery locust \
     psycopg2-binary
   ```
3. Configure PostgreSQL with the dev settings in `front/settings/dev.py`.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Common Commands
- Run tests:
  ```bash
  pytest
  ```y
- Start Celery worker:
  ```bash
  celery -A front worker -l info
  ```
- Start Celery beat:
  ```bash
  celery -A front beat -l info
  ```
- Run Locust:
  ```bash
  locust -f locustfiles/browse_products.py
  ```

## Notes / Gotchas
- Dev settings use a hardcoded `SECRET_KEY` and a local Postgres config.
- JWT auth uses `AUTH_HEADER_TYPES = ('JWT',)` (not `Bearer`).
- Media uploads use a custom file size validator in `store/valiodators.py`.
- `celerybeat-schedule.db` is tracked in git (runtime artifact).


