# ONA Platform - Complete Project Structure

## Repository File Tree

```
New-ONA/
│
├── README.md                          # Project overview and quick start
├── DEVELOPMENT_PLAN.md                # Complete 24-week development plan
├── ARCHITECTURE_SUMMARY.md            # Architecture quick reference
├── IMPLEMENTATION_GUIDE.md            # Code examples and setup guide
│
├── docker-compose.yml                 # Local development infrastructure
├── docker-compose.prod.yml            # Production deployment config
├── .env.example                       # Environment variables template
├── .gitignore
│
├── docs/                              # Additional documentation
│   ├── api/                           # API documentation
│   │   ├── endpoints.md
│   │   └── authentication.md
│   ├── deployment/
│   │   ├── kubernetes.md
│   │   └── aws-setup.md
│   └── user-guides/
│       ├── getting-started.md
│       └── data-ingestion.md
│
├── backend/                           # Python FastAPI backend
│   ├── requirements.txt               # Python dependencies
│   ├── pyproject.toml                 # Python project config
│   ├── pytest.ini                     # Test configuration
│   ├── .env                           # Environment variables (gitignored)
│   │
│   ├── api/                           # API Gateway Layer
│   │   ├── __init__.py
│   │   ├── gateway.py                 # FastAPI app initialization
│   │   ├── dependencies.py            # Shared dependencies
│   │   │
│   │   ├── routes/                    # API route modules
│   │   │   ├── __init__.py
│   │   │   ├── license_routes.py      # License validation endpoints
│   │   │   ├── data_routes.py         # Data ingestion endpoints
│   │   │   ├── graph_routes.py        # Graph analytics endpoints
│   │   │   ├── visualization_routes.py
│   │   │   └── export_routes.py
│   │   │
│   │   └── middleware/                # Middleware modules
│   │       ├── __init__.py
│   │       ├── auth_middleware.py     # API key validation
│   │       ├── tenant_middleware.py   # Multi-tenant isolation
│   │       ├── rate_limiter.py        # Rate limiting by tier
│   │       └── error_handler.py       # Global error handling
│   │
│   ├── services/                      # Business logic (modules only)
│   │   │
│   │   ├── ingestion/                 # Data ingestion services
│   │   │   ├── __init__.py
│   │   │   ├── neo4j_connector.py     # Neo4j connection functions
│   │   │   ├── sql_connector.py       # Relational DB connectors
│   │   │   ├── mysql_connector.py
│   │   │   ├── postgres_connector.py
│   │   │   ├── mssql_connector.py
│   │   │   ├── file_parser.py         # Edge file parsing functions
│   │   │   ├── csv_parser.py
│   │   │   ├── json_parser.py
│   │   │   ├── graphml_parser.py
│   │   │   ├── gexf_parser.py
│   │   │   ├── kafka_consumer.py      # Streaming data consumer
│   │   │   ├── batch_processor.py     # Batch upload handler
│   │   │   └── data_validator.py      # Input validation functions
│   │   │
│   │   ├── processing/                # Data transformation
│   │   │   ├── __init__.py
│   │   │   ├── data_transformer.py    # Data transformation functions
│   │   │   ├── graph_builder.py       # NetworkX graph construction
│   │   │   ├── edge_normalizer.py     # Normalize edge formats
│   │   │   ├── node_enricher.py       # Add computed node properties
│   │   │   └── filter_applier.py      # Apply trust score filters
│   │   │
│   │   ├── analytics/                 # Graph analytics (NetworkX)
│   │   │   ├── __init__.py
│   │   │   ├── graph_builder.py       # Build NetworkX graphs
│   │   │   ├── metrics_calculator.py  # Basic metrics functions
│   │   │   ├── centrality_analyzer.py # Centrality measures
│   │   │   ├── community_detector.py  # Community detection
│   │   │   ├── clique_finder.py       # Maximal cliques
│   │   │   ├── path_analyzer.py       # Shortest paths, recommendations
│   │   │   ├── efficiency_calculator.py
│   │   │   └── subgraph_extractor.py
│   │   │
│   │   ├── visualization/             # Visualization preprocessing
│   │   │   ├── __init__.py
│   │   │   ├── graph_preprocessor.py  # Prepare for react-force-graph
│   │   │   ├── layout_calculator.py   # Pre-compute layouts
│   │   │   ├── color_mapper.py        # Map attributes to colors
│   │   │   └── size_calculator.py     # Calculate node sizes
│   │   │
│   │   └── licensing/                 # License management
│   │       ├── __init__.py
│   │       ├── key_generator.py       # License key generation
│   │       ├── key_validator.py       # Key validation logic
│   │       ├── feature_gates.py       # Feature availability by tier
│   │       ├── tier_manager.py        # Tier configuration
│   │       └── usage_tracker.py       # Track API usage by account
│   │
│   ├── database/                      # Database operations (no ORM)
│   │   ├── __init__.py
│   │   ├── neo4j_ops.py               # Neo4j CRUD operations
│   │   ├── postgres_ops.py            # PostgreSQL operations
│   │   ├── mongo_ops.py               # MongoDB operations
│   │   ├── redis_ops.py               # Redis caching functions
│   │   └── migrations/                # Database migrations
│   │       ├── alembic.ini
│   │       ├── env.py
│   │       └── versions/
│   │
│   ├── models/                        # Pydantic data models
│   │   ├── __init__.py
│   │   ├── graph_schema.py            # Graph data models
│   │   ├── node_schema.py
│   │   ├── edge_schema.py
│   │   ├── license_schema.py          # License tier definitions
│   │   ├── tenant_schema.py           # Tenant/account models
│   │   ├── analytics_schema.py        # Analytics result models
│   │   └── api_responses.py           # API response models
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── logging_utils.py           # Logging configuration
│   │   ├── error_handlers.py          # Error handling functions
│   │   ├── config.py                  # Configuration management
│   │   ├── validators.py              # Input validation helpers
│   │   └── formatters.py              # Data formatting utilities
│   │
│   ├── tasks/                         # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py              # Celery configuration
│   │   ├── graph_tasks.py             # Long-running graph analytics
│   │   ├── batch_tasks.py             # Batch processing tasks
│   │   └── export_tasks.py            # Export generation tasks
│   │
│   └── tests/                         # Backend tests
│       ├── __init__.py
│       ├── conftest.py                # Pytest fixtures
│       ├── unit/                      # Unit tests
│       │   ├── test_neo4j_connector.py
│       │   ├── test_graph_analytics.py
│       │   └── test_license_validator.py
│       ├── integration/               # Integration tests
│       │   ├── test_api_endpoints.py
│       │   └── test_data_pipeline.py
│       └── fixtures/                  # Test data
│           ├── sample_graphs.json
│           └── test_edge_lists.csv
│
├── frontend/                          # React + TypeScript frontend
│   ├── package.json                   # Node dependencies
│   ├── package-lock.json
│   ├── tsconfig.json                  # TypeScript config
│   ├── vite.config.ts                 # Vite configuration
│   ├── .eslintrc.json                 # ESLint config
│   ├── .prettierrc                    # Prettier config
│   │
│   ├── public/                        # Static assets
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   └── demo-data/                 # Demo mode sample data
│   │       └── sample-graph.json
│   │
│   ├── src/
│   │   ├── main.tsx                   # Application entry point
│   │   ├── App.tsx                    # Root component
│   │   ├── index.css                  # Global styles
│   │   │
│   │   ├── components/                # React components
│   │   │   │
│   │   │   ├── layout/                # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── MainLayout.tsx
│   │   │   │
│   │   │   ├── visualization/         # Network visualization
│   │   │   │   ├── ForceGraph2D.tsx   # 2D graph wrapper
│   │   │   │   ├── ForceGraph3D.tsx   # 3D graph wrapper
│   │   │   │   ├── GraphControls.tsx  # Zoom, pan, layout
│   │   │   │   ├── GraphLegend.tsx    # Legend component
│   │   │   │   ├── NodeInfoPanel.tsx  # Node details panel
│   │   │   │   └── ViewToggle2D3D.tsx # 2D/3D toggle button
│   │   │   │
│   │   │   ├── data/                  # Data management components
│   │   │   │   ├── FileUploader.tsx   # File upload with drag-drop
│   │   │   │   ├── Neo4jConnector.tsx # Neo4j connection form
│   │   │   │   ├── SqlConnector.tsx   # SQL DB connection form
│   │   │   │   ├── KafkaConnector.tsx # Kafka stream setup
│   │   │   │   ├── DataSourceList.tsx # List of connected sources
│   │   │   │   ├── DataPreview.tsx    # Data table preview
│   │   │   │   └── FilterControls.tsx # Trust score, feature filters
│   │   │   │
│   │   │   ├── licensing/             # License components
│   │   │   │   ├── LicenseActivation.tsx  # Key input form
│   │   │   │   ├── DemoModeBanner.tsx     # Upgrade prompt
│   │   │   │   ├── FeatureGate.tsx        # Conditional rendering
│   │   │   │   ├── TierComparison.tsx     # Pricing table
│   │   │   │   └── UsageMetrics.tsx       # Account usage display
│   │   │   │
│   │   │   ├── analytics/             # Analytics components
│   │   │   │   ├── MetricsPanel.tsx   # Graph metrics display
│   │   │   │   ├── CentralityChart.tsx
│   │   │   │   ├── CommunityView.tsx
│   │   │   │   ├── TimeSeriesChart.tsx
│   │   │   │   ├── SankeyDiagram.tsx
│   │   │   │   └── RecommendationsPanel.tsx
│   │   │   │
│   │   │   └── common/                # Reusable components
│   │   │       ├── Button.tsx
│   │   │       ├── Card.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── LoadingSpinner.tsx
│   │   │       └── ErrorBoundary.tsx
│   │   │
│   │   ├── pages/                     # Page components
│   │   │   ├── LandingPage.tsx        # Landing with demo/activate
│   │   │   ├── DemoMode.tsx           # Demo mode interface
│   │   │   ├── ActivateLicense.tsx    # License activation page
│   │   │   ├── Dashboard.tsx          # Main dashboard
│   │   │   ├── DataSources.tsx        # Data source management
│   │   │   ├── NetworkViz.tsx         # Network visualization page
│   │   │   ├── Analytics.tsx          # Analytics page
│   │   │   ├── Reports.tsx            # Reports and exports
│   │   │   └── NotFound.tsx           # 404 page
│   │   │
│   │   ├── store/                     # Redux state management
│   │   │   ├── index.ts               # Store configuration
│   │   │   ├── hooks.ts               # Typed Redux hooks
│   │   │   ├── slices/
│   │   │   │   ├── licenseSlice.ts    # License state
│   │   │   │   ├── graphSlice.ts      # Graph visualization state
│   │   │   │   ├── dataSourceSlice.ts # Data sources state
│   │   │   │   ├── analyticsSlice.ts  # Analytics results
│   │   │   │   └── uiSlice.ts         # UI state (2D/3D toggle)
│   │   │   └── api/
│   │   │       ├── licenseApi.ts      # RTK Query: license endpoints
│   │   │       ├── dataApi.ts         # RTK Query: data endpoints
│   │   │       ├── graphApi.ts        # RTK Query: graph endpoints
│   │   │       └── analyticsApi.ts    # RTK Query: analytics endpoints
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useGraph.ts            # Graph state management
│   │   │   ├── useLicense.ts          # License validation
│   │   │   ├── useDataSource.ts       # Data source operations
│   │   │   └── useAnalytics.ts        # Analytics operations
│   │   │
│   │   ├── types/                     # TypeScript type definitions
│   │   │   ├── graph.ts               # Graph data types
│   │   │   ├── license.ts             # License types
│   │   │   ├── analytics.ts           # Analytics types
│   │   │   └── api.ts                 # API response types
│   │   │
│   │   ├── utils/                     # Utility functions
│   │   │   ├── graphUtils.ts          # Graph data transformations
│   │   │   ├── formatters.ts          # Data formatting
│   │   │   ├── validators.ts          # Input validation
│   │   │   └── constants.ts           # App constants
│   │   │
│   │   ├── styles/                    # Global styles
│   │   │   ├── theme.ts               # MUI theme config
│   │   │   └── global.css             # Global CSS
│   │   │
│   │   └── tests/                     # Frontend tests
│   │       ├── components/            # Component tests
│   │       ├── integration/           # Integration tests
│   │       └── e2e/                   # E2E tests (Playwright)
│   │
│   └── dist/                          # Build output (gitignored)
│
├── k8s/                               # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── neo4j-statefulset.yaml
│   ├── postgres-statefulset.yaml
│   ├── kafka-statefulset.yaml
│   ├── services.yaml
│   ├── ingress.yaml
│   └── hpa.yaml                       # Horizontal Pod Autoscaler
│
├── terraform/                         # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── vpc/
│   │   ├── eks/                       # Kubernetes cluster
│   │   ├── rds/                       # PostgreSQL
│   │   └── elasticache/               # Redis
│   └── environments/
│       ├── dev/
│       ├── staging/
│       └── production/
│
├── scripts/                           # Utility scripts
│   ├── setup-dev.sh                   # Development environment setup
│   ├── generate-license-key.py        # License key generator
│   ├── migrate-data.py                # Data migration script
│   ├── backup-neo4j.sh                # Neo4j backup
│   └── load-test.py                   # Load testing script
│
├── monitoring/                        # Monitoring configuration
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   │       ├── api-metrics.json
│   │       └── graph-analytics.json
│   └── alerts/
│       └── alert-rules.yml
│
└── .github/                           # GitHub Actions CI/CD
    └── workflows/
        ├── backend-tests.yml
        ├── frontend-tests.yml
        ├── build-and-deploy.yml
        └── security-scan.yml
```

---

## Key Directory Purposes

### `/backend`

Python FastAPI backend using **module-based architecture** (no classes). All business logic organized into functional modules for data ingestion, analytics, and licensing.

### `/frontend`

React + TypeScript SPA with Redux state management. Uses **react-force-graph-2d/3d** for WebGL-accelerated network visualization.

### `/docs`

Comprehensive documentation including API specs, deployment guides, and user manuals.

### `/k8s`

Kubernetes manifests for production deployment with auto-scaling, load balancing, and service mesh.

### `/terraform`

Infrastructure as Code for cloud provisioning (AWS/Azure/GCP).

### `/scripts`

Utility scripts for development, deployment, and maintenance tasks.

### `/monitoring`

Prometheus and Grafana configuration for observability.

---

## Module Organization Principle

All Python code follows a **functional, module-based pattern**:

```
✅ Functions in modules:
   services/analytics/metrics_calculator.py
   - calculate_density(graph) -> float
   - calculate_clustering(graph) -> float

❌ No class-based code:
   - No class GraphAnalyzer
   - No object instantiation
```

---

## Multi-Tenant Data Isolation

- **Neo4j**: Every node/edge labeled with `tenant_id`
- **PostgreSQL**: `account_id` column on all tables
- **API**: Middleware extracts tenant from license key

---

## Getting Started

1. Read [README.md](./README.md) for project overview
2. Review [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for roadmap
3. Check [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md) for design
4. Follow [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) for setup

---

**Last Updated**: January 6, 2026
