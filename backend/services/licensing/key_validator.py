"""License key validation module."""

from typing import Optional, Dict, Any
from datetime import datetime
import hashlib
import secrets


TIER_FEATURES = {
    "demo": {
        "data_input": False,
        "max_nodes": 100,
        "max_edges": 300,
        "export": False,
        "streaming": False,
        "3d_visualization": False,
        "api_calls_per_month": 100,
        "max_users": 1,
    },
    "basic": {
        "data_input": True,
        "max_nodes": 5000,
        "max_edges": 20000,
        "export": True,
        "streaming": False,
        "3d_visualization": True,
        "api_calls_per_month": 10000,
        "max_users": 5,
    },
    "professional": {
        "data_input": True,
        "max_nodes": 50000,
        "max_edges": 200000,
        "export": True,
        "streaming": True,
        "3d_visualization": True,
        "api_calls_per_month": 100000,
        "max_users": 25,
    },
    "enterprise": {
        "data_input": True,
        "max_nodes": None,  # Unlimited
        "max_edges": None,
        "export": True,
        "streaming": True,
        "3d_visualization": True,
        "api_calls_per_month": None,  # Unlimited
        "max_users": None,
    },
}


def generate_license_key() -> str:
    """
    Generate a new license key.

    Returns:
        32-character hex license key
    """
    return secrets.token_hex(16).upper()


def hash_license_key(key: str) -> str:
    """
    Hash license key for storage.

    Args:
        key: License key

    Returns:
        SHA256 hash of key
    """
    return hashlib.sha256(key.encode()).hexdigest()


def validate_license_key(key: str, db_query_func: Any) -> Optional[Dict[str, Any]]:
    """
    Validate license key and return tier information.

    Args:
        key: License key to validate
        db_query_func: Function to query database for license

    Returns:
        Dictionary with license info or None if invalid
    """
    if not key:
        # No key = demo mode
        return {
            "tier": "demo",
            "features": TIER_FEATURES["demo"],
            "account_id": "demo",
            "is_demo": True,
        }

    key_hash = hash_license_key(key)
    license_record = db_query_func(key_hash)

    if not license_record:
        return None

    # Check expiration
    if license_record.get("expires_at"):
        expires_at = license_record["expires_at"]
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)

        if expires_at < datetime.utcnow():
            return None

    tier = license_record.get("tier", "basic")

    return {
        "tier": tier,
        "features": TIER_FEATURES.get(tier, TIER_FEATURES["basic"]),
        "account_id": license_record["account_id"],
        "is_demo": False,
        "expires_at": license_record.get("expires_at"),
    }


def check_feature_access(license_info: Dict[str, Any], feature: str) -> bool:
    """
    Check if license has access to a feature.

    Args:
        license_info: License information dictionary
        feature: Feature name to check

    Returns:
        True if feature is accessible, False otherwise
    """
    features = license_info.get("features", {})
    return features.get(feature, False)


def check_limit(
    license_info: Dict[str, Any], limit_name: str, current_value: int
) -> bool:
    """
    Check if current value exceeds license limit.

    Args:
        license_info: License information dictionary
        limit_name: Name of limit (e.g., "max_nodes")
        current_value: Current value to check

    Returns:
        True if within limit, False if exceeded
    """
    features = license_info.get("features", {})
    limit = features.get(limit_name)

    if limit is None:  # Unlimited
        return True

    return current_value <= limit
