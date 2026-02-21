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
