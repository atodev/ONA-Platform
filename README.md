![ONA Platform](ONA-P.png)

# ONA Platform

> **Enterprise-Grade Organizational Network Analysis** - React.js frontend with Python FastAPI backend and multi-source graph database architecture

---

## 📋 Project Overview

This repository contains the complete development plan for a scalable, enterprise-grade organizational network analysis platform with:

- **React 18 + TypeScript** frontend with WebGL-accelerated 3D network visualization
- **Python FastAPI** backend using modular (non-class) architecture
- **Neo4j graph database** for primary data storage with multi-tenant isolation
- **Multi-source data ingestion**: Neo4j, SQL databases, edge files, and streaming (Kafka)
- **API key-based licensing** with Demo/Basic/Professional/Enterprise tiers

---

## 📚 Documentation Structure

This project includes comprehensive planning and implementation documentation:

### Core Planning Documents

1. **[DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)** ⭐ _Start Here_

   - Complete 24-week development roadmap
   - 10 phases with detailed milestones and 200+ todos
   - Team structure, budget estimates, risk management
   - Success metrics and KPIs

2. **[ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)** 🏗️

   - Quick reference guide for architecture decisions
   - Technology stack breakdown
   - Data flow diagrams
   - Module structure and patterns
   - License tier feature matrix
   - Deployment architecture

3. **[ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md)** 🏗️

   - Quick reference guide for architecture decisions
   - Technology stack breakdown
   - Data flow diagrams
   - Module structure and patterns
   - License tier feature matrix
   - Deployment architecture

4. **[SCALABILITY_ANALYSIS.md](./SCALABILITY_ANALYSIS.md)** 📈

   - How to scale from 100 to 100,000+ users
   - Component-by-component scaling strategies
   - Cost analysis at different scales
   - Performance bottlenecks and solutions
   - Real-world deployment scenarios
   - Load testing recommendations

5. **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** 💻
   - Getting started with local development
   - Docker Compose setup for all services
   - Complete code examples for Python modules
   - React component examples
   - Step-by-step setup instructions

---

## 🏗️ Architecture Highlights

### Frontend Stack

```
React 18 + TypeScript
├── react-force-graph-2d/3d (WebGL visualization)
├── Redux Toolkit (state management)
├── Material-UI (components)
└── Vite (build tool)
```

### Backend Stack (Python Modules Only - No Classes)

```
FastAPI (API Gateway)
├── Data Ingestion Service
│   ├── Neo4j connector
│   ├── SQL connectors (PostgreSQL, MySQL, MSSQL)
│   ├── File parsers (CSV, JSON, GraphML, GEXF)
│   └── Kafka consumer (streaming)
├── Graph Analytics Service (NetworkX)
├── License Management Service
└── Visualization Preprocessing Service
```

### Data Layer

```
Neo4j (primary graph database, multi-tenant)
PostgreSQL (licenses, tenants, metadata)
MongoDB (preprocessed graph data)
Redis (caching, rate limiting)
Apache Kafka (streaming ingestion)
```

---

## 🔐 Licensing Model

### Tier Comparison

| Feature               | Demo | Basic            | Professional   | Enterprise      |
| --------------------- | ---- | ---------------- | -------------- | --------------- |
| **Price**             | Free | $99/mo           | $499/mo        | Custom          |
| **Data Input**        | ❌   | ✅ Files + Neo4j | ✅ All sources | ✅ All + APIs   |
| **Max Nodes**         | 100  | 5,000            | 50,000         | Unlimited       |
| **3D Visualization**  | ❌   | ✅               | ✅             | ✅              |
| **Streaming (Kafka)** | ❌   | ❌               | ✅             | ✅              |
| **Export**            | ❌   | ✅               | ✅             | ✅              |
| **API Access**        | ❌   | Read-only        | Full           | Full + webhooks |
| **Users**             | 1    | 5                | 25             | Unlimited       |

**Demo Mode Features:**

- Read-only sample datasets
- Basic 2D visualization (100 nodes max)
- Watermarked visualizations
- No data input capabilities

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 1. Start Infrastructure

```bash
# Start all services (Neo4j, PostgreSQL, MongoDB, Redis, Kafka)
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python api/gateway.py
```

### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474

---

## 📊 Key Features

### Multi-Source Data Ingestion

- ✅ **Neo4j Direct Connection** - Query existing graph databases
- ✅ **Relational Databases** - SQL queries from PostgreSQL, MySQL, MSSQL
- ✅ **Edge Files** - CSV, JSON, GraphML, GEXF formats
- ✅ **Streaming Data** - Real-time ingestion via Apache Kafka
- ✅ **Batch Uploads** - Large file processing with progress tracking

### Advanced Network Visualization

- ✅ **2D/3D Toggle** - WebGL-accelerated rendering
- ✅ **Force-Directed Layouts** - Interactive physics simulation
- ✅ **Custom Styling** - Node size/color by attributes
- ✅ **Path Highlighting** - Show connections between nodes
- ✅ **Large Graph Support** - Optimized for 50K+ nodes

### Graph Analytics

- ✅ **Centrality Measures** - Degree, betweenness, closeness, eigenvector
- ✅ **Community Detection** - Louvain algorithm
- ✅ **Clique Detection** - Find maximal cliques
- ✅ **Network Metrics** - Density, clustering, efficiency
- ✅ **Path Analysis** - Shortest paths, triadic closure

### Multi-Tenant Architecture

- ✅ **Account Isolation** - Data separated by tenant_id
- ✅ **Neo4j Labels** - Tenant-specific node/edge labels
- ✅ **API Key Validation** - Per-request tenant identification
- ✅ **Usage Tracking** - Per-account metrics and quotas

---

## 🛠️ Technology Stack

### Frontend

- React 18.2+
- TypeScript 5.0+
- react-force-graph-2d/3d
- Redux Toolkit + RTK Query
- Material-UI v5
- Vite 5.0+

### Backend (Python Modules - No Classes)

- FastAPI 0.109+
- NetworkX 3.2+
- Pandas 2.1+
- Neo4j Python Driver 5.15+
- Pydantic 2.5+
- Celery 5.3+

### Infrastructure

- Neo4j 5.15 (graph database)
- PostgreSQL 16 (relational)
- MongoDB 7 (document store)
- Redis 7 (cache)
- Apache Kafka 3.6 (streaming)
- Docker & Kubernetes

---

## 📅 Project Timeline

| Phase     | Duration      | Description                            |
| --------- | ------------- | -------------------------------------- |
| Phase 1-2 | Weeks 1-5     | Foundation, backend services           |
| Phase 3-4 | Weeks 6-9     | Frontend foundation, data management   |
| Phase 5-6 | Weeks 10-15   | Network visualization, advanced charts |
| Phase 7   | Weeks 16-18   | Streaming integration, collaboration   |
| Phase 8-9 | Weeks 19-22   | Performance optimization, testing      |
| Phase 10  | Weeks 23-24   | Deployment, launch                     |
| **Total** | **~6 months** | **Full production release**            |

---

## 👥 Team Requirements

### Core Team (Recommended)

- 1x Tech Lead / Architect
- 2x Senior Full-Stack Developers
- 1x Frontend Developer (React specialist)
- 1x Backend Developer (Python specialist)
- 1x DevOps Engineer
- 1x UI/UX Designer
- 1x QA Engineer
- 1x Product Manager

---

## 💰 Budget Estimate

### Development (6 months)

- Team: $400K - $600K
- Infrastructure: $5K - $10K
- Tools/Services: $5K - $10K
- **Total**: ~$410K - $620K

### Annual Operating Costs

- Infrastructure: $30K - $60K (includes Neo4j Enterprise, Kafka)
- Maintenance: $100K - $150K
- Monitoring: $5K - $10K
- Security: $10K - $20K
- Neo4j License: $15K - $30K
- **Total**: ~$160K - $270K/year

---

## 🔒 Security & Compliance

- ✅ API key-based authentication
- ✅ Multi-tenant data isolation (Neo4j labels + query filters)
- ✅ Rate limiting per license tier
- ✅ Encrypted data at rest and in transit
- ✅ Audit logging
- ✅ OWASP Top 10 compliance
- ✅ Regular security scans

---

## 📈 Performance Targets

- **API Response Time**: < 200ms (p95)
- **Graph Load Time**: < 2s for 10K nodes
- **Streaming Latency**: < 100ms (ingestion to storage)
- **Concurrent Users**: 10,000+
- **Throughput**: 1,000 requests/second
- **Uptime**: 99.9%

---

## 🔄 Data Flow

```
External Sources → Ingestion Layer → Storage Layer → Processing → Frontend
     │                    │                │             │            │
Neo4j/SQL/Files → Connectors/Parsers → Neo4j (tenant) → Analytics → react-force-graph
                           │                                            2D/3D
                      Kafka Stream → MongoDB (cache)
```

---

## 📖 Key Design Principles

### 1. Module-Based Python (No Classes)

```python
# ✅ PREFER: Pure functions
def calculate_metrics(graph: nx.Graph) -> dict:
    return {"density": nx.density(graph)}

# ❌ AVOID: Classes
class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph
```

### 2. Multi-Tenant Isolation

- Every Neo4j node/edge has `tenant_id` property
- All queries filter by `tenant_id`
- API middleware extracts tenant from license key

### 3. License-Gated Features

- Demo mode: No key required, limited features
- Licensed modes: Key required, features by tier
- Frontend checks license before rendering components

### 4. Scalability First

- Horizontal scaling for all services
- Caching at multiple layers (Redis, MongoDB)
- Async processing for heavy workloads (Celery)

---

## 🧪 Testing Strategy

- **Unit Tests**: 80%+ coverage for Python modules
- **Integration Tests**: API endpoints, database operations
- **E2E Tests**: Playwright/Cypress for critical user flows
- **Load Tests**: JMeter/Locust for performance validation
- **Security Tests**: OWASP Top 10 scanning

---

## 🚢 Deployment

### Development

```bash
docker-compose -f docker-compose.dev.yml up
```

### Production (Kubernetes)

```bash
kubectl apply -f k8s/
```

### Monitoring

- Prometheus (metrics)
- Grafana (dashboards)
- ELK Stack (logging)
- Sentry (error tracking)

---

## 📝 Contributing

This is a planning and architecture repository. Implementation will follow the guidelines in the documentation.

### Development Workflow

1. Review [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for current phase
2. Check [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md) for design patterns
3. Follow code examples in [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
4. Write tests for all new code
5. Submit PR with documentation updates

---

## 📞 Support & Contact

- **Technical Questions**: See documentation in this repository
- **Architecture Decisions**: Refer to ARCHITECTURE_SUMMARY.md
- **Implementation Help**: Check IMPLEMENTATION_GUIDE.md

---

## 📄 License

[Add your license here]

---

## ✅ Current Status

**Project Phase**: Planning Complete ✅  
**Next Step**: Begin Phase 1 - Foundation & Setup  
**Documentation Version**: 2.0  
**Last Updated**: January 6, 2026

---

## 🗺️ Roadmap

- [x] ✅ Architecture design
- [x] ✅ Technology stack selection
- [x] ✅ Development plan creation
- [x] ✅ Documentation complete
- [ ] ⏭️ Phase 1: Foundation setup
- [ ] ⏭️ Phase 2: Core backend services
- [ ] ⏭️ Phase 3: Frontend foundation
- [ ] ⏭️ Phase 4-10: Feature development → Launch

---

**Ready to build the next generation of Organizational Network Analysis!** 🚀
