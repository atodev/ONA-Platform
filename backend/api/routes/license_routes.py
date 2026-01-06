"""License validation and management routes"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/license", tags=["license"])


class LicenseValidation(BaseModel):
    api_key: str


class LicenseInfo(BaseModel):
    tier: str
    features: list[str]
    max_nodes: int
    expires_at: str | None = None


@router.post("/validate", response_model=LicenseInfo)
async def validate_license(license: LicenseValidation):
    """Validate API key and return license tier information"""
    # TODO: Implement actual license validation
    # Placeholder response for demo
    return {
        "tier": "demo",
        "features": ["view_graph", "basic_metrics"],
        "max_nodes": 1000,
        "expires_at": None,
    }


@router.get("/tiers")
async def get_license_tiers():
    """Get available license tiers and features"""
    return {
        "demo": {
            "price": 0,
            "max_nodes": 1000,
            "features": ["view_graph", "basic_metrics"],
            "data_input": False,
        },
        "basic": {
            "price": 99,
            "max_nodes": 10000,
            "features": ["view_graph", "basic_metrics", "csv_upload", "export"],
            "data_input": True,
        },
        "professional": {
            "price": 499,
            "max_nodes": 100000,
            "features": [
                "view_graph",
                "advanced_metrics",
                "multi_source",
                "streaming",
                "api_access",
                "collaboration",
            ],
            "data_input": True,
        },
        "enterprise": {
            "price": "custom",
            "max_nodes": "unlimited",
            "features": [
                "all_features",
                "white_label",
                "sso",
                "dedicated_support",
                "sla",
            ],
            "data_input": True,
        },
    }
