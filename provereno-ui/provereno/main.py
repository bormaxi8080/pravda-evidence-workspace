"""FastAPI application factory."""
from __future__ import annotations
from contextlib import asynccontextmanager
from pathlib import Path
from sqlalchemy import text

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from provereno.database import engine

from provereno.routers import auth, snapshots, job_routes, export, collections, public, pages


def _datetimefmt(dt) -> str:
    if dt is None: return "—"
    try: return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception: return str(dt)

def _datetimeshort(dt) -> str:
    if dt is None: return "—"
    try: return dt.strftime("%d.%m %H:%M")
    except Exception: return str(dt)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema migration and isolated workers are separate operator-owned steps.
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="Provereno UI", lifespan=lifespan)

PACKAGE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))
templates.env.filters["datetimefmt"]   = _datetimefmt
templates.env.filters["datetimeshort"] = _datetimeshort
app.state.templates = templates

app.mount("/static", StaticFiles(directory=str(PACKAGE_DIR / "static")), name="static")

app.include_router(auth.router)
app.include_router(job_routes.router)
app.include_router(snapshots.router)
app.include_router(export.router)
app.include_router(collections.router)
app.include_router(public.router)
app.include_router(pages.router)
