"""API route modules for ONA Platform"""

from .license_routes import router as license_router
from .data_routes import router as data_router
from .graph_routes import router as graph_router

__all__ = ["license_router", "data_router", "graph_router"]
