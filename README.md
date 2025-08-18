```md
# Auth Demo: FastAPI + SQLite (efímero)

**Objetivo:** API de autenticación con JWT + Refresh, ideal para demo sin datos persistentes.

## Endpoints principales
- `POST /auth/register` { email, password }
- `POST /auth/login` { email, password } → tokens
- `POST /auth/refresh` { refresh_token }
- `GET  /users/me` (Bearer access token)

## Ejecutar local
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\\Scripts\\activate)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Visita `http://localhost:8000/docs`.

## Modo demo sin persistencia
Establece `DEMO_RESET=1` para que **cada arranque** borre y recree `db.sqlite3`.

## Deploy en Render
1. Subir repo a GitHub.
2. Crear **Web Service** en Render.
3. Variables de entorno (copiar desde `.env.example`).
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
6. (Opcional) En `render.yaml` puedes automatizar.

## Seguridad (demo)
- Contraseñas con bcrypt.
- JWT (access/refresh) con expiración.
- **Nota:** Es una demo. No incluye:
  - Rotación de refresh tokens (se puede agregar)
  - Rate limiting (se puede agregar con `slowapi`)
  - Verificación de email real (mockeable)
```
