# Stage 2: Implementation Next Steps

## Current Status

✅ **Completed (Stage 1):**

- Backend API Gateway (FastAPI) with health endpoints
- License validation routes (tiers, validation)
- Data ingestion routes (upload, connect sources)
- Graph analytics routes (query, metrics, communities)
- Docker Compose environment (Neo4j, PostgreSQL, MongoDB, Redis, Kafka)
- Vite + React + TypeScript frontend scaffolding
- Force-directed graph visualization component stub

🟢 **Services Running:**

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend dev ready: port 5173

---

## Next Steps: Choose Your Path

### Path A: Complete the Frontend (Best for UI Demo) 🎨

**Goal:** Create an interactive, visually impressive demo for stakeholders

**Tasks:**

1. **Start the frontend dev server**

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

2. **Implement the ForceGraph2D component** (`frontend/src/components/visualization/ForceGraph2D.tsx`)

   - Connect to `/api/v1/graph/query` endpoint
   - Display sample network visualization
   - Add basic controls (zoom, pan, node selection)
   - Style nodes by group/community
   - Add tooltips with node information

3. **Create data upload UI** (`frontend/src/components/data/UploadForm.tsx`)

   - File upload form for CSV/JSON
   - Connect to `/api/v1/data/upload` endpoint
   - Show upload progress and status
   - Display validation errors

4. **Build license tier selector** (`frontend/src/components/license/TierSelector.tsx`)
   - Display available tiers from `/api/v1/license/tiers`
   - Show feature comparison matrix
   - Implement API key input field

**Estimated Time:** 6-8 hours  
**Outcome:** Interactive web app you can demo to investors

---

### Path B: Implement Core Backend Services (Best for Technical Foundation) 🔧

**Goal:** Build robust backend services with real database connections

**Tasks:**

1. **Neo4j Connector** (`backend/services/ingestion/neo4j_connector.py`)

   - Implement `connect()` - establish Neo4j connection
   - Implement `store_graph(nodes, edges, tenant_id)` - save graph data with tenant isolation
   - Implement `query_nodes(tenant_id, filters)` - retrieve graph data
   - Implement `delete_graph(tenant_id)` - cleanup operations
   - Add connection pooling and error handling
   - Test with running Neo4j instance (http://localhost:7474)

2. **License Validator** (`backend/services/licensing/key_validator.py`)

   - Create PostgreSQL schema:
     ```sql
     CREATE TABLE licenses (
       id UUID PRIMARY KEY,
       api_key_hash VARCHAR(255) UNIQUE,
       tier VARCHAR(50),
       max_nodes INTEGER,
       features JSONB,
       expires_at TIMESTAMP,
       tenant_id UUID
     );
     ```
   - Implement `validate_license_key(api_key, db_query_func)` - hash and validate key
   - Implement `check_tier_limits(license_info, operation)` - enforce node limits, features
   - Add key generation utilities for testing

3. **Metrics Calculator** (`backend/services/analytics/metrics_calculator.py`)

   - Implement `calculate_centrality(graph, metric_type)` - degree, betweenness, eigenvector, PageRank
   - Implement `detect_communities(graph, algorithm)` - Louvain, label propagation
   - Implement `calculate_clustering_coefficient(graph)`
   - Return results in react-force-graph format (nodes with `val` property for sizing)
   - Add NetworkX integration

4. **Update API routes** to use real services instead of placeholders
   - Modify `graph_routes.py` to call Neo4j connector
   - Modify `license_routes.py` to use license validator
   - Modify `data_routes.py` to process uploads and store in Neo4j

**Estimated Time:** 12-16 hours  
**Outcome:** Production-ready backend services with database persistence

---

### Path C: Create Working End-to-End Demo (Best for Quick Win) 🚀 ⭐ **RECOMMENDED**

**Goal:** Vertical slice from data upload → database → visualization

**Tasks:**

1. **Create sample network data** (`backend/data/samples/`)

   - `karate_club.csv` - Zachary's Karate Club (34 nodes, 78 edges)
   - `corporate_network.csv` - Mock corporate network (100 nodes, 300 edges)
   - `email_network.json` - Sample email interaction data
   - Document CSV format: `source,target,weight,type`

2. **Implement simplified Neo4j connector** (`backend/services/ingestion/neo4j_connector.py`)

   - Focus on: `store_graph()` and `query_graph()`
   - Use tenant_id labels for isolation: `(:Person:tenant_abc {id: "1"})`
   - Simple Cypher queries (no optimization yet)

3. **Build CSV ingestion endpoint** (`backend/api/routes/data_routes.py`)

   - Parse uploaded CSV file
   - Validate format (required columns: source, target)
   - Call Neo4j connector to store graph
   - Return ingestion summary (nodes/edges created)

4. **Implement graph query endpoint** (`backend/api/routes/graph_routes.py`)

   - Query Neo4j for all nodes/edges for tenant
   - Transform to react-force-graph format:
     ```json
     {
       "nodes": [{ "id": "1", "name": "Alice", "group": 1 }],
       "links": [{ "source": "1", "target": "2", "value": 1 }]
     }
     ```
   - Limit to 1000 nodes for demo tier

5. **Connect frontend to backend** (`frontend/src/components/visualization/ForceGraph2D.tsx`)

   - Add `useEffect` to fetch data from `/api/v1/graph/query`
   - Pass data to `ForceGraph2D` component
   - Handle loading and error states
   - Add refresh button

6. **Create upload flow** (`frontend/src/App.tsx`)
   - Add file upload button
   - POST to `/api/v1/data/upload`
   - Refresh graph after successful upload
   - Show success/error messages

**Estimated Time:** 8-10 hours  
**Outcome:** Fully functional demo - upload CSV → see visualization → impress investors

---

## Recommended: Path C - End-to-End Demo

### Why Path C First?

1. **Investor-Ready:** Something tangible to show in meetings
2. **Validates Architecture:** Proves the tech stack works together
3. **Quick Feedback:** See if the visualization performs as expected
4. **Motivation:** Working software is motivating for the team
5. **Agile Methodology:** Vertical slice > horizontal layers

### Implementation Order

```
Day 1: Backend Services (4-5 hours)
├── Create sample CSV data
├── Implement Neo4j connector (basic)
├── Update data_routes.py for CSV upload
└── Update graph_routes.py to query Neo4j

Day 2: Frontend Integration (4-5 hours)
├── Fetch graph data from API
├── Wire up ForceGraph2D component
├── Create upload UI
└── Test end-to-end flow

Day 3: Polish & Demo (2-3 hours)
├── Add loading states
├── Error handling
├── Basic styling
└── Prepare demo script
```

---

## After Path C Completion

### Next Phase: Expand Features

1. **Add more visualizations**

   - 3D force graph (`react-force-graph-3d`)
   - Node filtering by properties
   - Zoom to selected node

2. **Implement basic analytics**

   - Calculate centrality metrics
   - Highlight top influential nodes
   - Show community colors

3. **Add license enforcement**

   - Node count limits by tier
   - Feature gates (demo can't upload)
   - API key validation

4. **Improve data ingestion**
   - Support JSON, GraphML formats
   - Add data validation
   - Show ingestion progress

---

## Success Criteria for Stage 2

✅ Upload a CSV file with network data  
✅ Data persists in Neo4j database  
✅ Graph visualization displays nodes and edges  
✅ Can interact with graph (pan, zoom, select nodes)  
✅ Demo runs without errors on localhost  
✅ Ready to show investors in under 5 minutes

---

## Resources Needed

**For Path C:**

- Running Docker containers (already ✅)
- Neo4j Python driver (`pip install neo4j`)
- Pandas for CSV parsing (`pip install pandas`)
- React hooks knowledge (useState, useEffect)
- 8-10 hours of development time

**Sample Data Sources:**

- Zachary's Karate Club: https://networkx.org/documentation/stable/auto_examples/graph/plot_karate_club.html
- Stanford Network Data: http://snap.stanford.edu/data/
- Generate synthetic with NetworkX: `nx.barabasi_albert_graph(100, 3)`

---

## Getting Started

**To begin Path C:**

1. Create sample data directory:

   ```powershell
   mkdir backend/data/samples
   ```

2. Install Python dependencies:

   ```powershell
   cd backend
   pip install neo4j pandas networkx
   ```

3. Verify Neo4j is accessible:

   - Open http://localhost:7474
   - Login with neo4j/password
   - Run: `MATCH (n) RETURN count(n)`

4. Ready to implement! 🚀

---

**Questions? Issues? Next Steps?**

Choose your path and let's build! 💪
