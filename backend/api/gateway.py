"""FastAPI application gateway."""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

app = FastAPI(
    title="ONA Platform API",
    version="2.0.0",
    description="Organizational Network Analysis Platform",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency: License validation
async def validate_api_key(x_api_key: Optional[str] = Header(None)):
    """Validate API key from header."""
    # TODO: Implement license validation with database
    # from services.licensing.key_validator import validate_license_key
    # from database.postgres_ops import query_license_by_hash
    # license_info = validate_license_key(x_api_key, query_license_by_hash)

    # Placeholder for now
    if not x_api_key:
        return {"tier": "demo", "max_nodes": 1000}

    return {"tier": "basic", "max_nodes": 10000}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "ONA Platform API v2.0", "status": "operational"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
from api.routes import license_routes, data_routes, graph_routes

app.include_router(license_routes.router)
app.include_router(data_routes.router)
app.include_router(graph_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
