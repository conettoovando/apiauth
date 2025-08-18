from fastapi import FastAPI
from app.db.init_db import init_db, reset_if_demo
from app.routes import auth, users

app = FastAPI(title="Auth Demo (FastAPI + SQLite)")

# Reset the database if in demo mode
reset_if_demo()
# Initialize the database (create tables)
init_db()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs"}


