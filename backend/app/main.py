from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.api.health import router as health_router
from backend.app.api.sessions import router as sessions_router
from backend.app.api.jobs import router as jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup directories
    settings.sessions_dir.mkdir(parents=True, exist_ok=True)
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="Shadow Arena",
    description="Markas Emosi Debat Multi-Agent ML",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(health_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")


@app.get("/api/demo")
async def get_demo_debate():
    demo_path = settings.data_dir / "demo_titanic.debate.json"
    if not demo_path.exists():
        raise HTTPException(status_code=404, detail="Demo debate belum digenerate. Jalankan scripts/make_demo.py.")
    return FileResponse(demo_path, media_type="application/json")


# Serve static frontend
frontend_dir = settings.frontend_dir

if frontend_dir.exists():
    css_dir = frontend_dir / "css"
    js_dir = frontend_dir / "js"
    if css_dir.exists():
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if js_dir.exists():
        app.mount("/js", StaticFiles(directory=js_dir), name="js")


@app.get("/")
async def serve_index():
    index_file = settings.frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse({"status": "Shadow Arena Backend Active", "docs": "/docs"})
