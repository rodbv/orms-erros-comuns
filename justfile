run:
    uv run python manage.py runserver

test *args:
    uv run pytest {{args}}

migrate:
    uv run python manage.py migrate

mmm:
    uv run python manage.py makemigrations
    uv run python manage.py migrate

m *args:
    uv run python manage.py {{args}}

slides:
    cd slides && npm run dev -- --remote --port 3030

slides-install:
    cd slides && npm install

slides-build:
    cd slides && npm run build

frontend-install:
    cd frontend && npm install

frontend:
    cd frontend && (sleep 2 && (xdg-open http://localhost:3000 || open http://localhost:3000) >/dev/null 2>&1 &) && npm run dev -- --host --port 3000

app:
    #!/usr/bin/env bash
    set -euo pipefail
    uv run python manage.py runserver >/tmp/orms-erros-comuns-backend.log 2>&1 &
    backend_pid=$!
    trap 'kill "$backend_pid"' EXIT INT TERM
    cd frontend
    (sleep 2 && (xdg-open http://localhost:3000 || open http://localhost:3000) >/dev/null 2>&1 &)
    npm run dev -- --host --port 3000

reseed:
    uv run python manage.py seed --clear
