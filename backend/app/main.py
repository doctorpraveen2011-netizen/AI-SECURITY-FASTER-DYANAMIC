import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
from app.database.seed import seed_all_data

# Import all API routers
from app.api.dashboard import router as dashboard_router
from app.api.llm_routes import router as llm_router
from app.api.rag_routes import router as rag_router
from app.api.agent_routes import router as agent_router
from app.api.redteam_routes import router as redteam_router
from app.api.blueteam_routes import router as blueteam_router
from app.api.mcp_routes import router as mcp_router
from app.api.wazuh_routes import router as wazuh_router
from app.api.reports_routes import router as reports_router
from app.api.audit_routes import router as audit_router
from app.api.settings_routes import router as settings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_all_data(db)
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Red Teaming & Blue Teaming Operations Center",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all endpoints under /api
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(llm_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(agent_router, prefix=settings.API_V1_STR)
app.include_router(redteam_router, prefix=settings.API_V1_STR)
app.include_router(blueteam_router, prefix=settings.API_V1_STR)
app.include_router(mcp_router, prefix=settings.API_V1_STR)
app.include_router(wazuh_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
app.include_router(settings_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI SECURITY FASTER API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "AI SECURITY FASTER"}
