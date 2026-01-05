# ONA Platform - Architecture Summary

## Quick Reference Guide

### 🎯 Core Architecture Decisions

#### Frontend

- **React 18 + TypeScript**
- **react-force-graph-2d** - Primary 2D visualization (WebGL-accelerated)
- **react-force-graph-3d** - Primary 3D visualization (Three.js/WebGL)
- **Material-UI** - Component library
- **Redux Toolkit** - State management

#### Backend

- **Python FastAPI** - API Gateway
- **Module-based architecture** - No classes, functional programming only
- **Microservices** - Independently scalable services

#### Data Sources (Multi-Input)

```
┌─────────────────────────────────────────────────┐
│            Data Input Sources                   │
├─────────────────────────────────────────────────┤
│ 1. Neo4j Graph Database (direct connection)    │
│ 2. Relational DBs (PostgreSQL, MySQL, MSSQL)   │
│ 3. Edge Files (CSV, JSON, GraphML, GEXF)       │
│ 4. Streaming (Apache Kafka - vendor feeds)     │
│ 5. Batch Uploads (large files)                 │
└─────────────────────────────────────────────────┘
```

#### Data Storage

- **Neo4j** - Primary graph database (multi-tenant with labels)
- **PostgreSQL** - License management, tenant metadata
- **MongoDB** - Preprocessed graph data for react-force-graph
- **Redis** - Caching, rate limiting, sessions

#### Message Queue

- **Apache Kafka** - Streaming data ingestion from vendors

---

## 🔐 Licensing Model

### API Key-Based Tiers

| Tier             | Key Required | Data Input              | Max Nodes | Price   |
| ---------------- | ------------ | ----------------------- | --------- | ------- |
| **Demo**         | ❌ No        | Read-only samples       | 100       | Free    |
| **Basic**        | ✅ Yes       | File upload + Neo4j     | 5,000     | $99/mo  |
| **Professional** | ✅ Yes       | All sources + streaming | 50,000    | $499/mo |
| **Enterprise**   | ✅ Yes       | All sources + APIs      | Unlimited | Custom  |

### Demo Mode Features

- Read-only access to sample datasets
- Basic 2D visualization (100 node limit)
- Watermarked visualizations
- No data export
- No data input capabilities

### Licensed Mode Features

- Full data input from all sources
- Unlimited graph size (based on tier)
- Export to all formats
- API access
- Real-time collaboration
- No watermarks

---

## 📊 Data Flow Architecture

```
External Sources          Ingestion Layer         Storage Layer        Processing         Frontend
─────────────────         ───────────────         ─────────────        ──────────         ────────

┌──────────────┐         ┌───────────────┐       ┌──────────┐        ┌──────────┐       ┌────────┐
│   Neo4j DB   │────────>│ neo4j_        │──────>│  Neo4j   │───────>│  Graph   │──────>│ React  │
│  (External)  │         │ connector.py  │       │ (Multi-  │        │ Analytics│       │ Force  │
└──────────────┘         └───────────────┘       │ Tenant)  │        │ Service  │       │ Graph  │
                                                  └──────────┘        └──────────┘       │ 2D/3D  │
┌──────────────┐         ┌───────────────┐             │                   │            └────────┘
│ Relational   │────────>│ sql_          │             │                   │
│ DBs (SQL)    │         │ connector.py  │             │                   ▼
└──────────────┘         └───────────────┘       ┌──────────┐        ┌──────────┐
                                                  │ MongoDB  │<───────│  Visual  │
┌──────────────┐         ┌───────────────┐       │(Preproc) │        │  Preproc │
│  CSV/JSON    │────────>│ file_         │       └──────────┘        │ Service  │
│  Edge Files  │         │ parser.py     │             │             └──────────┘
└──────────────┘         └───────────────┘       ┌──────────┐
                                                  │PostgreSQL│
┌──────────────┐         ┌───────────────┐       │(Licenses)│
│ Kafka Stream │────────>│ kafka_        │       └──────────┘
│ (Vendors)    │         │ consumer.py   │             │
└──────────────┘         └───────────────┘       ┌──────────┐
                                │                 │  Redis   │
                                │                 │ (Cache)  │
                                ▼                 └──────────┘
                         ┌───────────────┐
                         │Apache Kafka   │
                         │ Message Queue │
                         └───────────────┘
```

---

## 🏗️ Python Module Structure (No Classes)

### Service Modules Organization

```python
backend/
├── api/
│   ├── gateway.py                    # FastAPI app
│   └── routes/
│       ├── license_routes.py         # GET /license/validate
│       ├── data_routes.py            # POST /data/ingest
│       └── graph_routes.py           # GET /graph/metrics
│
├── services/
│   ├── ingestion/
│   │   ├── neo4j_connector.py        # fetch_graph(), write_graph()
│   │   ├── sql_connector.py          # connect_db(), query_edges()
│   │   ├── file_parser.py            # parse_csv(), parse_json()
│   │   ├── kafka_consumer.py         # consume_stream(), validate_message()
│   │   └── batch_processor.py        # process_batch(), chunk_file()
│   │
│   ├── analytics/
│   │   ├── graph_builder.py          # build_graph(), add_edges()
│   │   ├── metrics_calculator.py     # calc_density(), calc_clustering()
│   │   ├── centrality_analyzer.py    # calc_betweenness(), calc_degree()
│   │   └── community_detector.py     # detect_communities(), find_cliques()
│   │
│   └── licensing/
│       ├── key_validator.py          # validate_key(), get_features()
│       └── feature_gates.py          # check_feature(), enforce_limit()
│
└── database/
    ├── neo4j_ops.py                  # create_connection(), run_query()
    ├── postgres_ops.py               # query(), insert(), update()
    └── redis_ops.py                  # cache_get(), cache_set()
```

### Example Function Signature Patterns

```python
# services/ingestion/neo4j_connector.py
def fetch_graph_by_tenant(
    driver: neo4j.Driver,
    tenant_id: str,
    filters: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Fetch graph edges for a specific tenant."""
    pass

# services/analytics/metrics_calculator.py
def calculate_basic_metrics(graph: nx.Graph) -> Dict[str, float]:
    """Calculate density, clustering, and transitivity."""
    pass

# services/licensing/key_validator.py
def validate_license_key(
    key: str,
    db_connection: Any
) -> Optional[Dict[str, Any]]:
    """Validate license key and return tier info."""
    pass
```

---

## 🔄 Data Ingestion Workflows

### 1. CSV File Upload (Licensed Users)

```
User uploads CSV → API Gateway → License validation →
File parser → Graph builder → Neo4j storage → Return success
```

### 2. Neo4j Direct Connection

```
User provides credentials → Connection test → Cypher query →
Extract subgraph → Transform to standard format →
Store in tenant-isolated namespace → Cache in MongoDB
```

### 3. Streaming from Kafka (Professional+)

```
Vendor publishes to Kafka → Consumer polls topic →
Validate message schema → Buffer edges →
Batch write to Neo4j → Update real-time via WebSocket
```

### 4. Relational DB Query

```
User configures SQL connection → Run edge query →
Transform SQL results to graph format →
Write to Neo4j with tenant label → Preprocess for visualization
```

---

## 🎨 Frontend Component Structure

```
src/
├── components/
│   ├── visualization/
│   │   ├── ForceGraph2D.tsx          # react-force-graph-2d wrapper
│   │   ├── ForceGraph3D.tsx          # react-force-graph-3d wrapper
│   │   ├── GraphControls.tsx         # Zoom, pan, layout controls
│   │   └── GraphLegend.tsx           # Node/edge legend
│   │
│   ├── data/
│   │   ├── FileUploader.tsx          # CSV/JSON upload
│   │   ├── Neo4jConnector.tsx        # Neo4j connection form
│   │   ├── SqlConnector.tsx          # SQL DB connection form
│   │   └── DataPreview.tsx           # Data table preview
│   │
│   ├── licensing/
│   │   ├── LicenseActivation.tsx     # Key input form
│   │   ├── DemoModeBanner.tsx        # "Upgrade to unlock" banner
│   │   └── FeatureGate.tsx           # Conditional feature rendering
│   │
│   └── analytics/
│       ├── MetricsPanel.tsx          # Display graph metrics
│       ├── TimeSeriesChart.tsx       # Temporal analysis
│       └── SankeyDiagram.tsx         # Flow visualization
│
└── store/
    ├── licenseSlice.ts               # License state & validation
    ├── graphSlice.ts                 # Graph data & visualization state
    └── dataSourceSlice.ts            # Connected data sources
```

---

## 🔒 Multi-Tenant Isolation Strategy

### Neo4j Tenant Isolation

```cypher
// Every node and relationship tagged with tenant_id
CREATE (n:Node:Customer {id: "user123", tenant_id: "acme_corp"})
CREATE (m:Node:Customer {id: "user456", tenant_id: "acme_corp"})
CREATE (n)-[r:EDGE {tenant_id: "acme_corp", weight: 0.85}]->(m)

// Query always filters by tenant
MATCH (n:Node {tenant_id: $tenant_id})-[r:EDGE {tenant_id: $tenant_id}]->(m)
RETURN n, r, m
```

### PostgreSQL Tenant Isolation

```sql
-- Row-level security
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    data JSONB
);

CREATE INDEX idx_datasets_account ON datasets(account_id);

-- Application enforces WHERE account_id = current_account
```

### API Gateway Isolation

```python
# middleware/tenant_middleware.py
async def enforce_tenant_isolation(request: Request):
    """Extract and validate tenant from license key."""
    api_key = request.headers.get("X-API-Key")
    license_info = validate_license_key(api_key)

    if not license_info:
        raise HTTPException(status_code=401)

    request.state.account_id = license_info['account_id']
    request.state.tier = license_info['tier']
```

---

## 📈 Scalability Strategy

### Horizontal Scaling Points

1. **API Gateway** - Multiple instances behind load balancer
2. **Neo4j** - Causal cluster (3+ core servers)
3. **Kafka** - Multiple brokers with partitioning
4. **Redis** - Redis Cluster or Sentinel
5. **Graph Analytics** - Celery workers on separate nodes

### Performance Targets

- **API Response**: < 200ms (p95)
- **Graph Load**: < 2s for 10K nodes
- **Streaming Latency**: < 100ms ingestion to storage
- **Concurrent Users**: 10,000+
- **Throughput**: 1,000 requests/second

---

## 🚀 Deployment Architecture

```
                        ┌──────────────┐
                        │  CloudFlare  │
                        │  CDN + WAF   │
                        └──────┬───────┘
                               │
                        ┌──────▼───────┐
                        │Load Balancer │
                        └──────┬───────┘
                ┌──────────────┼──────────────┐
                │              │              │
         ┌──────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
         │ API Gateway │ │   API    │ │    API     │
         │  Instance 1 │ │Instance 2│ │ Instance 3 │
         └──────┬──────┘ └────┬─────┘ └─────┬──────┘
                │              │              │
         ┌──────┴──────────────┴──────────────┴─────┐
         │                                           │
    ┌────▼─────────┐  ┌──────────────┐  ┌──────────▼───┐
    │   Neo4j      │  │    Kafka     │  │  PostgreSQL  │
    │   Cluster    │  │   Cluster    │  │  + Replicas  │
    │ (3 servers)  │  │ (3 brokers)  │  └──────────────┘
    └──────────────┘  └──────────────┘
         │
    ┌────▼─────────┐  ┌──────────────┐
    │   MongoDB    │  │    Redis     │
    │  Replica Set │  │   Cluster    │
    └──────────────┘  └──────────────┘
```

---

## 📝 Key Implementation Notes

### Critical Design Decisions

1. ✅ **Python modules only** - No classes, pure functions
2. ✅ **Multi-source ingestion** - Neo4j, SQL, files, streams
3. ✅ **Neo4j as primary** - Graph database for customer data
4. ✅ **react-force-graph** - WebGL for performance
5. ✅ **API key licensing** - Demo/Basic/Pro/Enterprise tiers
6. ✅ **Tenant isolation** - Labels in Neo4j, account_id everywhere
7. ✅ **Kafka for streaming** - Vendor data feeds
8. ✅ **Demo mode** - No data input, sample data only

### Technology Constraints

- **No OOP classes** in Python backend
- **No JWT/OAuth** - API keys only
- **Multi-tenant required** - Account isolation enforced at all layers
- **Streaming required** - Kafka for vendor integrations

---

**Version**: 2.0  
**Last Updated**: January 6, 2026  
**Status**: Approved Architecture
