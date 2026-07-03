# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Turnero is a Flask-based appointment/scheduling management system (in Spanish). It manages `Cliente` (customers), `Servicio` (services), and `Turno` (appointments) that link a customer to a service at a given date/time with a status.

## Commands

Activate the venv first (Windows): `venv\Scripts\activate` (PowerShell: `venv\Scripts\Activate.ps1`).

- Run the dev server: `flask --app app run` (or `python app.py` is NOT wired up — there's no `if __name__ == "__main__"` block, always use `flask --app app run`)
- Create a migration after changing a model: `flask db migrate -m "description"`
- Apply migrations: `flask db upgrade`
- Install dependencies: `pip install -r requirements.txt`

There are no tests, linter, or build step configured in this repository.

## Architecture

Standard Flask app factory-less setup, single `app.py` entrypoint:

- `app.py` creates the `Flask` app, configures the SQLite DB (`sqlite:///turnero.db`), initializes `Flask-SQLAlchemy` and `Flask-Migrate`, and registers each blueprint. **Any new blueprint must be imported and registered here explicitly** — it's a common mistake to add a blueprint under `routes/` and forget to register it, which silently makes all its routes 404.
- `models/db.py` holds the single shared `db = SQLAlchemy()` instance imported by every model — always import `db` from here, never instantiate a new one.
- `models/` — one file per entity (`cliente.py`, `servicio.py`, `turno.py`), plus `estados_turno.py` which defines the `EstadoTurno` string constants (`Pendiente`, `Confirmado`, `Cancelado`, `Realizado`) used as the `Turno.estado` values. `Turno` has required (`nullable=False`) foreign keys to both `Cliente` and `Servicio`.
- `routes/` — one blueprint per entity, each prefixed with its own URL prefix (`/clientes`, `/servicios`, `/turnos`). Routes read form fields directly via `request.form[...]` (no form library/validation layer) and call `db.session.commit()` inline — there's no service layer.
- `templates/` — Jinja2 templates organized by entity in matching subfolders (`clientes/`, `servicios/`, `turnos/`, `dashboard/`), all extending `templates/base.html`.
- `migrations/` — standard Alembic/Flask-Migrate setup; `migrations/versions/` holds the migration history and must stay in sync with the models.
- Soft-delete pattern: `Cliente` and `Servicio` both use an `activo` boolean flag (toggled via `/desactivar` and `/activar` routes) instead of hard deletes. `Turno` doesn't have `activo` — its lifecycle is tracked via the `estado` field instead (e.g., cancellation sets `estado` to `Cancelado`, it isn't deleted or deactivated).
