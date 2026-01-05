# ONA Platform - Implementation Quick Start

## Getting Started with Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Neo4j Desktop (for local development)
- Git

---

## Local Development Setup

### 1. Clone and Initialize

```bash
# Clone repository
git clone <repository-url>
cd New-ONA

# Create directory structure
mkdir -p backend/{api,services,database,models,utils}
mkdir -p backend/services/{ingestion,analytics,licensing,visualization}
mkdir -p frontend/{src,public}
```

### 2. Backend Setup (Python)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn neo4j psycopg2-binary pymongo redis kafka-python
pip install networkx pandas pydantic python-multipart
pip install celery pytest black

# Create .env file
cat > .env << EOF
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
POSTGRES_URI=postgresql://user:password@localhost:5432/ona
MONGODB_URI=mongodb://localhost:27017/ona
REDIS_URI=redis://localhost:6379
KAFKA_BROKERS=localhost:9092
SECRET_KEY=your-secret-key-here
EOF
```

### 3. Frontend Setup (React)

```bash
# Navigate to frontend
cd frontend

# Initialize React app with Vite
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install
npm install @reduxjs/toolkit react-redux
npm install react-force-graph-2d react-force-graph-3d
npm install @mui/material @emotion/react @emotion/styled
npm install react-router-dom
npm install recharts d3
npm install axios

# Install dev dependencies
npm install -D @types/d3 @types/react-router-dom
```

### 4. Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: "3.9"

services:
  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.15-enterprise
    ports:
      - "7474:7474" # Browser UI
      - "7687:7687" # Bolt
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_server_memory_heap_max__size: 4G
    volumes:
      - neo4j_data:/data

  # PostgreSQL
  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ona
      POSTGRES_USER: onauser
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # MongoDB
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Kafka
  kafka:
    image: bitnami/kafka:3.6
    ports:
      - "9092:9092"
    environment:
      KAFKA_CFG_NODE_ID: 1
      KAFKA_CFG_PROCESS_ROLES: broker,controller
      KAFKA_CFG_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CFG_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CFG_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093
      ALLOW_PLAINTEXT_LISTENER: yes
    volumes:
      - kafka_data:/bitnami/kafka

volumes:
  neo4j_data:
  postgres_data:
  mongo_data:
  redis_data:
  kafka_data:
```

Start all services:

```bash
docker-compose up -d
```

---

## Backend Module Examples

### Example 1: Neo4j Connector Module

`backend/services/ingestion/neo4j_connector.py`:

```python
"""Neo4j graph database connector module."""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver
import logging

logger = logging.getLogger(__name__)


def create_driver(uri: str, user: str, password: str) -> Driver:
    """
    Create Neo4j driver instance.

    Args:
        uri: Neo4j connection URI (bolt://...)
        user: Database username
        password: Database password

    Returns:
        Neo4j driver instance
    """
    return GraphDatabase.driver(uri, auth=(user, password))


def test_connection(driver: Driver) -> bool:
    """
    Test Neo4j connection.

    Args:
        driver: Neo4j driver instance

    Returns:
        True if connection successful, False otherwise
    """
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            return result.single()["test"] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


def fetch_graph_edges(
    driver: Driver,
    tenant_id: str,
    node_label: str = "Node",
    edge_type: str = "EDGE",
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Fetch graph edges for a specific tenant.

    Args:
        driver: Neo4j driver instance
        tenant_id: Tenant identifier for data isolation
        node_label: Label for nodes (default: "Node")
        edge_type: Type for relationships (default: "EDGE")
        filters: Optional filters (e.g., {"min_weight": 0.5})

    Returns:
        List of edge dictionaries with source, target, properties
    """
    filters = filters or {}
    min_weight = filters.get("min_weight", 0.0)

    query = f"""
    MATCH (source:{node_label} {{tenant_id: $tenant_id}})
          -[edge:{edge_type} {{tenant_id: $tenant_id}}]->
          (target:{node_label} {{tenant_id: $tenant_id}})
    WHERE edge.weight >= $min_weight
    RETURN
        source.id AS source_id,
        target.id AS target_id,
        edge.weight AS weight,
        properties(edge) AS edge_props,
        properties(source) AS source_props,
        properties(target) AS target_props
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(
            query,
            tenant_id=tenant_id,
            min_weight=min_weight,
            limit=filters.get("limit", 10000)
        )

        return [
            {
                "source": record["source_id"],
                "target": record["target_id"],
                "weight": record["weight"],
                "edge_properties": record["edge_props"],
                "source_properties": record["source_props"],
                "target_properties": record["target_props"]
            }
            for record in result
        ]


def write_graph_edges(
    driver: Driver,
    tenant_id: str,
    edges: List[Dict[str, Any]],
    node_label: str = "Node",
    edge_type: str = "EDGE"
) -> Dict[str, int]:
    """
    Write graph edges to Neo4j with tenant isolation.

    Args:
        driver: Neo4j driver instance
        tenant_id: Tenant identifier
        edges: List of edge dicts with 'source', 'target', 'weight', etc.
        node_label: Label for nodes
        edge_type: Type for relationships

    Returns:
        Dictionary with counts of nodes/edges created
    """
    query = f"""
    UNWIND $edges AS edge
    MERGE (source:{node_label} {{id: edge.source, tenant_id: $tenant_id}})
    MERGE (target:{node_label} {{id: edge.target, tenant_id: $tenant_id}})
    MERGE (source)-[rel:{edge_type} {{tenant_id: $tenant_id}}]->(target)
    SET rel.weight = edge.weight,
        rel.updated_at = datetime()
    """

    with driver.session() as session:
        result = session.run(query, edges=edges, tenant_id=tenant_id)
        summary = result.consume()

        return {
            "nodes_created": summary.counters.nodes_created,
            "relationships_created": summary.counters.relationships_created,
            "properties_set": summary.counters.properties_set
        }


def delete_tenant_data(driver: Driver, tenant_id: str) -> int:
    """
    Delete all data for a specific tenant.

    Args:
        driver: Neo4j driver instance
        tenant_id: Tenant identifier

    Returns:
        Number of nodes deleted
    """
    query = """
    MATCH (n {tenant_id: $tenant_id})
    DETACH DELETE n
    RETURN count(n) AS deleted_count
    """

    with driver.session() as session:
        result = session.run(query, tenant_id=tenant_id)
        return result.single()["deleted_count"]
```

### Example 2: Graph Metrics Calculator Module

`backend/services/analytics/metrics_calculator.py`:

```python
"""Graph metrics calculation module (no classes)."""
import networkx as nx
from typing import Dict, Any, List


def calculate_basic_metrics(graph: nx.Graph) -> Dict[str, Any]:
    """
    Calculate basic network metrics.

    Args:
        graph: NetworkX graph instance

    Returns:
        Dictionary of metric name -> value
    """
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "avg_clustering": nx.average_clustering(graph),
        "transitivity": nx.transitivity(graph),
        "is_connected": nx.is_connected(graph)
    }


def calculate_centrality_metrics(graph: nx.Graph) -> Dict[str, Dict[str, float]]:
    """
    Calculate centrality measures for all nodes.

    Args:
        graph: NetworkX graph instance

    Returns:
        Dictionary of centrality type -> {node: score}
    """
    return {
        "degree": dict(nx.degree_centrality(graph)),
        "betweenness": dict(nx.betweenness_centrality(graph)),
        "closeness": dict(nx.closeness_centrality(graph)),
        "eigenvector": dict(nx.eigenvector_centrality(graph, max_iter=1000))
    }


def find_top_nodes_by_centrality(
    graph: nx.Graph,
    centrality_type: str = "degree",
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Find top N nodes by centrality measure.

    Args:
        graph: NetworkX graph instance
        centrality_type: Type of centrality ("degree", "betweenness", etc.)
        top_n: Number of top nodes to return

    Returns:
        List of {node, score} dictionaries
    """
    centrality_funcs = {
        "degree": nx.degree_centrality,
        "betweenness": nx.betweenness_centrality,
        "closeness": nx.closeness_centrality,
        "eigenvector": nx.eigenvector_centrality
    }

    if centrality_type not in centrality_funcs:
        raise ValueError(f"Unknown centrality type: {centrality_type}")

    centrality = centrality_funcs[centrality_type](graph)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

    return [
        {"node": node, "score": score}
        for node, score in sorted_nodes[:top_n]
    ]


def detect_communities(graph: nx.Graph) -> List[List[str]]:
    """
    Detect communities using Louvain algorithm.

    Args:
        graph: NetworkX graph instance

    Returns:
        List of communities (each is a list of node IDs)
    """
    import networkx.algorithms.community as nx_comm

    communities = nx_comm.louvain_communities(graph)
    return [list(community) for community in communities]


def find_largest_cliques(graph: nx.Graph, top_n: int = 5) -> List[List[str]]:
    """
    Find the largest cliques in the graph.

    Args:
        graph: NetworkX graph instance
        top_n: Number of largest cliques to return

    Returns:
        List of cliques (each is a list of node IDs)
    """
    cliques = list(nx.find_cliques(graph))
    cliques.sort(key=len, reverse=True)
    return [list(clique) for clique in cliques[:top_n]]


def calculate_shortest_path(
    graph: nx.Graph,
    source: str,
    target: str
) -> Dict[str, Any]:
    """
    Calculate shortest path between two nodes.

    Args:
        graph: NetworkX graph instance
        source: Source node ID
        target: Target node ID

    Returns:
        Dictionary with path and length
    """
    try:
        path = nx.shortest_path(graph, source, target)
        length = nx.shortest_path_length(graph, source, target)

        return {
            "path": path,
            "length": length,
            "exists": True
        }
    except nx.NetworkXNoPath:
        return {
            "path": [],
            "length": float('inf'),
            "exists": False
        }
```

### Example 3: License Validator Module

`backend/services/licensing/key_validator.py`:

```python
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
        "max_users": 1
    },
    "basic": {
        "data_input": True,
        "max_nodes": 5000,
        "max_edges": 20000,
        "export": True,
        "streaming": False,
        "3d_visualization": True,
        "api_calls_per_month": 10000,
        "max_users": 5
    },
    "professional": {
        "data_input": True,
        "max_nodes": 50000,
        "max_edges": 200000,
        "export": True,
        "streaming": True,
        "3d_visualization": True,
        "api_calls_per_month": 100000,
        "max_users": 25
    },
    "enterprise": {
        "data_input": True,
        "max_nodes": None,  # Unlimited
        "max_edges": None,
        "export": True,
        "streaming": True,
        "3d_visualization": True,
        "api_calls_per_month": None,  # Unlimited
        "max_users": None
    }
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


def validate_license_key(
    key: str,
    db_query_func: Any
) -> Optional[Dict[str, Any]]:
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
            "is_demo": True
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
        "expires_at": license_record.get("expires_at")
    }


def check_feature_access(
    license_info: Dict[str, Any],
    feature: str
) -> bool:
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
    license_info: Dict[str, Any],
    limit_name: str,
    current_value: int
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
```

---

## FastAPI Application Structure

`backend/api/gateway.py`:

```python
"""FastAPI application gateway."""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

app = FastAPI(
    title="ONA Platform API",
    version="2.0.0",
    description="Organizational Network Analysis Platform"
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
    from services.licensing.key_validator import validate_license_key
    from database.postgres_ops import query_license_by_hash

    license_info = validate_license_key(x_api_key, query_license_by_hash)

    if not license_info:
        raise HTTPException(status_code=401, detail="Invalid or expired license key")

    return license_info


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

app.include_router(license_routes.router, prefix="/api/v1/license", tags=["license"])
app.include_router(data_routes.router, prefix="/api/v1/data", tags=["data"])
app.include_router(graph_routes.router, prefix="/api/v1/graph", tags=["graph"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

---

## Frontend React Component Example

`frontend/src/components/visualization/ForceGraph2D.tsx`:

```typescript
import React, { useRef, useCallback } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { GraphData } from "../../types/graph";

interface ForceGraph2DProps {
  data: GraphData;
  onNodeClick?: (node: any) => void;
  onNodeHover?: (node: any) => void;
  height?: number;
  width?: number;
}

export const ForceGraph2DComponent: React.FC<ForceGraph2DProps> = ({
  data,
  onNodeClick,
  onNodeHover,
  height = 600,
  width = 800,
}) => {
  const forceRef = useRef<any>();

  const handleNodeClick = useCallback(
    (node: any) => {
      if (onNodeClick) {
        onNodeClick(node);
      }

      // Center camera on node
      if (forceRef.current) {
        forceRef.current.centerAt(node.x, node.y, 1000);
        forceRef.current.zoom(2, 1000);
      }
    },
    [onNodeClick]
  );

  const nodeCanvasObject = useCallback(
    (node: any, ctx: CanvasRenderingContext2D) => {
      // Custom node rendering
      const size = node.size || 5;
      const color = node.color || "#1976d2";

      // Draw node
      ctx.beginPath();
      ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();

      // Draw label
      if (node.label) {
        ctx.font = "10px Arial";
        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.fillText(node.label, node.x, node.y + size + 12);
      }
    },
    []
  );

  return (
    <ForceGraph2D
      ref={forceRef}
      graphData={data}
      height={height}
      width={width}
      nodeLabel="id"
      nodeColor={(node: any) => node.color || "#1976d2"}
      nodeRelSize={5}
      linkColor={() => "rgba(255,255,255,0.2)"}
      linkWidth={(link: any) => Math.sqrt(link.weight || 1)}
      onNodeClick={handleNodeClick}
      onNodeHover={onNodeHover}
      nodeCanvasObject={nodeCanvasObject}
      cooldownTicks={100}
      onEngineStop={() => forceRef.current?.zoomToFit(400)}
    />
  );
};
```

---

## Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate
python api/gateway.py
# API runs on http://localhost:8000
```

### Start Frontend

```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### Access Services

- **API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **Frontend**: http://localhost:5173

---

## Next Implementation Steps

1. ✅ Set up development environment
2. ✅ Initialize project structure
3. ⏭️ Implement Neo4j connector module
4. ⏭️ Implement license validator module
5. ⏭️ Create FastAPI routes
6. ⏭️ Build React force graph component
7. ⏭️ Add demo mode UI
8. ⏭️ Implement data ingestion pipeline

---

**Last Updated**: January 6, 2026
