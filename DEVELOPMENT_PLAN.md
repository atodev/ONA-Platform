# ONA Platform Modernization - Development Plan

## React.js Frontend with Modern Backend Architecture

---

## Executive Summary

Modernization of the existing Streamlit-based Organizational Network Analysis (ONA) application into a scalable, enterprise-grade platform using React.js for the frontend and a microservices-based backend architecture.

### Current Application Overview

The existing Streamlit application provides:

- CSV dataset upload and processing
- Network visualization using PyVis
- Sankey diagrams for flow analysis
- Time series analysis of organizational communications
- NetworkX-based graph analytics (clustering, density, efficiency, cliques)
- Trust score filtering
- Multi-dimensional feature selection and correlation

---

## Technology Stack

### Frontend

- **Framework**: React 18+ with TypeScript
- **State Management**: Redux Toolkit + RTK Query
- **UI Components**: Material-UI (MUI) v5 or Ant Design
- **Visualization**:
  - **react-force-graph-2d** (primary 2D network visualization)
  - **react-force-graph-3d** (primary 3D network visualization)
  - Recharts/Victory for charts and time series
  - D3.js for custom supplementary visualizations
  - React-Flow for Sankey/flow diagrams
- **Build Tool**: Vite
- **Testing**: Jest + React Testing Library
- **Code Quality**: ESLint, Prettier, Husky

### Backend

- **API Gateway**: FastAPI (Python) - functional/modular design (no classes)
- **Microservices** (Python modules only):
  - **Data Ingestion Service** - Multi-source data connectors:
    - Neo4j graph database connector
    - Relational DB connectors (PostgreSQL, MySQL, SQL Server)
    - Edge file parsers (CSV, JSON, GraphML, GEXF)
    - Streaming data processor (Kafka consumers)
    - Batch upload handler
  - **Data Processing Service** - Pandas, NetworkX for transformations
  - **Graph Analytics Service** - NetworkX, igraph for analysis
  - **Tenant Isolation Service** - Multi-tenant data segregation by account
  - **Visualization Service** - Graph preprocessing for react-force-graph
  - **License Management Service** - Key validation and feature gating
- **Database**:
  - **Neo4j** (primary graph database for customer data)
  - **PostgreSQL** (tenant management, licensing, metadata)
  - **MongoDB** (document store for preprocessed graph data)
  - **Redis** (caching, session management, rate limiting)
- **Message Queue**: Apache Kafka (streaming input from vendors)
- **Task Queue**: Celery (for long-running analytics)
- **Authentication**: API Key-based licensing (no OAuth for customers)
- **API Documentation**: OpenAPI/Swagger

### Infrastructure & DevOps

- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production) / Docker Swarm (staging)
- **CI/CD**: GitHub Actions or GitLab CI
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Cloud Platform**: AWS/Azure/GCP (cloud-agnostic design)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│   React.js SPA - react-force-graph-2d/3d - Material-UI         │
│            Demo Mode (no key) | Full Mode (with key)            │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS/WSS
┌────────────────────────┴────────────────────────────────────────┐
│                     API Gateway Layer                            │
│              FastAPI (Python modules) + Load Balancer           │
│                   API Key Validation Middleware                 │
└────┬──────────┬──────────────┬──────────────┬──────────────────┘
     │          │              │              │
┌────┴─────┐ ┌─┴───────────┐ ┌┴──────────┐ ┌┴──────────────────┐
│ License  │ │  Data       │ │  Graph    │ │ Visualization     │
│ Service  │ │  Ingestion  │ │  Analytics│ │ Preprocessing     │
│ (Keys)   │ │  Service    │ │  Service  │ │ (force-graph fmt) │
└──────────┘ └─────┬───────┘ └─────┬─────┘ └───────────────────┘
                   │               │
          ┌────────┴───────────────┴────────┐
          │   Apache Kafka (Message Queue)  │
          │  - Vendor streaming ingestion   │
          │  - Batch processing queue       │
          └────────┬────────────────────────┘
                   │
     ┌─────────────┼─────────────┬───────────────┐
     │             │             │               │
┌────┴──────┐ ┌───┴─────┐ ┌─────┴─────┐ ┌───────┴────────┐
│   Neo4j   │ │  Postgres│ │  MongoDB  │ │     Redis      │
│ (Customer │ │ (Tenants,│ │ (Preproc  │ │  (Cache/Rate   │
│  Graphs   │ │ Licenses)│ │  Graphs)  │ │   Limiting)    │
│ Multi-    │ │          │ │           │ │                │
│ Tenant)   │ │          │ │           │ │                │
└───────────┘ └──────────┘ └───────────┘ └────────────────┘
     ▲             ▲
     │             │
┌────┴──────┐ ┌────┴──────────┐
│ External  │ │  Relational   │
│ Neo4j DB  │ │  DBs (MySQL,  │
│ Sources   │ │  PostgreSQL)  │
└───────────┘ └───────────────┘

        Data Input Sources:
        • CSV/JSON/GraphML edge files
        • Neo4j direct connection
        • Relational DB queries
        • Kafka streaming (vendors)
        • Batch file uploads
```

---

## Development Phases & Milestones

### **Phase 1: Foundation & Setup** (Weeks 1-2)

#### Milestone 1.1: Project Initialization

- [ ] Set up monorepo structure (Nx/Turborepo or Lerna)
- [ ] Initialize frontend React + TypeScript project with Vite
- [ ] Set up backend FastAPI project structure
- [ ] Configure Docker development environment
- [ ] Set up version control and branching strategy
- [ ] Create project documentation structure
- [ ] Set up CI/CD pipeline basics

#### Milestone 1.2: Development Environment

- [ ] Configure ESLint, Prettier, and pre-commit hooks
- [ ] Set up database containers (PostgreSQL, MongoDB, Redis)
- [ ] Configure environment variables management
- [ ] Set up hot-reload for frontend and backend
- [ ] Create docker-compose.yml for local development
- [ ] Set up API documentation framework (Swagger/OpenAPI)

#### Milestone 1.3: License Management & Authentication Framework

- [ ] Design license key schema (tiers: Demo, Basic, Professional, Enterprise)
- [ ] Implement API key generation and validation
- [ ] Create license key activation endpoints
- [ ] Build key validation middleware for feature gating
- [ ] Create demo mode UI (read-only, sample data)
- [ ] Create license key entry/activation UI
- [ ] Implement license tier feature matrix
- [ ] Add license expiration and renewal handling
- [ ] Create admin license management dashboard
- [ ] Implement rate limiting by license tier

---

### **Phase 2: Core Backend Services** (Weeks 3-5)

#### Milestone 2.1: API Gateway & Routing

- [ ] Design RESTful API structure
- [ ] Implement API gateway with FastAPI
- [ ] Set up rate limiting and throttling
- [ ] Configure CORS policies
- [ ] Implement request/response logging
- [ ] Create API versioning strategy
- [ ] Set up health check endpoints

#### Milestone 2.2: Data Ingestion Service (Multi-Source Connectors)

- [ ] **Neo4j Connector Module**:
  - [ ] Implement Cypher query builder
  - [ ] Create graph extraction functions
  - [ ] Add connection pooling and error handling
- [ ] **Relational DB Connector Module**:
  - [ ] PostgreSQL connector with SQL query builder
  - [ ] MySQL connector
  - [ ] SQL Server connector
  - [ ] Generic SQL to graph transformation
- [ ] **Edge File Parser Module**:
  - [ ] CSV edge list parser (source, target, weight)
  - [ ] JSON graph format parser
  - [ ] GraphML parser
  - [ ] GEXF parser
  - [ ] File validation and error handling
- [ ] **Streaming Data Module**:
  - [ ] Kafka consumer for vendor streams
  - [ ] Real-time data validation
  - [ ] Stream-to-graph transformation
  - [ ] Backpressure handling
- [ ] **Batch Upload Handler**:
  - [ ] Large file chunking and processing
  - [ ] Progress tracking
  - [ ] Resumable uploads
- [ ] **Tenant Isolation Module**:
  - [ ] Account-based data segregation
  - [ ] Neo4j label/namespace strategy per tenant
  - [ ] Query isolation enforcement
- [ ] Unit tests for all ingestion modules (85%+ coverage)

#### Milestone 2.3: Data Processing Service

- [ ] Create data transformation pipeline (module-based)
- [ ] Implement trust score filtering functionality
- [ ] Implement feature selection logic
- [ ] Add data caching with Redis
- [ ] Create data export functionality
- [ ] Build graph normalization functions
- [ ] Add data quality validation
- [ ] Unit tests for data processing (80%+ coverage)

#### Milestone 2.4: Graph Analytics Service (Python Modules Only)

- [ ] Create modular graph analytics functions (no classes):
  - [ ] `graph_builder.py` - NetworkX graph construction from multiple sources
  - [ ] `metrics_calculator.py` - Node/edge counting, density, clustering
  - [ ] `centrality_analyzer.py` - Degree, betweenness, closeness centrality
  - [ ] `community_detector.py` - Community detection algorithms
  - [ ] `clique_finder.py` - Clique detection functions
  - [ ] `path_analyzer.py` - Shortest paths, triadic closure recommendations
  - [ ] `efficiency_calculator.py` - Global/local efficiency metrics
- [ ] Optimize graph algorithms for large datasets (100K+ nodes)
- [ ] Add Redis caching for computed metrics
- [ ] Create Celery task wrappers for heavy computations
- [ ] Implement graph subsampling for performance
- [ ] Unit and integration tests for all modules

#### Milestone 2.5: Database Models & Multi-Tenant Architecture

- [ ] **Neo4j Graph Database**:
  - [ ] Design multi-tenant graph schema with labels
  - [ ] Create indexes for performance (account_id, node_id)
  - [ ] Implement Cypher query templates
  - [ ] Set up connection pool management
- [ ] **PostgreSQL Schema** (functional approach, no ORM classes):
  - [ ] Tenants/accounts table
  - [ ] License keys and tiers table
  - [ ] Usage metrics and audit logs
  - [ ] Data source configurations
- [ ] **MongoDB Schema**:
  - [ ] Preprocessed graph data for react-force-graph
  - [ ] Cached analytics results
  - [ ] User preferences by account
- [ ] Implement database migrations (Alembic)
- [ ] Create seed data for demo mode
- [ ] Add database indexing strategy
- [ ] Implement automated backup procedures
- [ ] Set up read replicas for scaling

---

### **Phase 3: Frontend Foundation** (Weeks 4-6)

#### Milestone 3.1: UI Component Library

- [ ] Set up Material-UI theme and customization
- [ ] Create base components:
  - [ ] Layout (Header, Sidebar, Footer)
  - [ ] Navigation components
  - [ ] Form components (File upload, Select, Slider)
  - [ ] Button variants
  - [ ] Card components
  - [ ] Modal/Dialog components
- [ ] Implement responsive design system
- [ ] Create component documentation (Storybook)

#### Milestone 3.2: State Management

- [ ] Configure Redux Toolkit store
- [ ] Set up RTK Query for API integration
- [ ] Create feature slices:
  - [ ] License/authentication slice (key validation state)
  - [ ] Dataset slice (account-isolated data)
  - [ ] Graph visualization slice (2D/3D toggle state)
  - [ ] Analytics slice
  - [ ] UI state slice (demo mode vs licensed mode)
- [ ] Implement local storage persistence (license key caching)
- [ ] Add error handling and retry logic

#### Milestone 3.3: Routing & Navigation

- [ ] Set up React Router v6
- [ ] Create route structure:
  - [ ] `/` - Landing page with demo/license activation
  - [ ] `/demo` - Demo mode (sample data, read-only)
  - [ ] `/activate` - License key activation
  - [ ] `/datasets` - Dataset management (licensed only)
  - [ ] `/analyze` - Analysis workspace
  - [ ] `/network` - Network visualization (2D/3D)
  - [ ] `/reports` - Reports and exports (licensed only)
- [ ] Implement license-gated routes (demo vs full access)
- [ ] Add breadcrumb navigation
- [ ] Create 404/error pages with upgrade prompts

---

### **Phase 4: Core Features - Data Management** (Weeks 7-9)

#### Milestone 4.1: Multi-Source Data Input & Management

- [ ] **File Upload Interface**:
  - [ ] Drag-and-drop for CSV/JSON/GraphML/GEXF files
  - [ ] Upload progress indicators
  - [ ] File format validation and preview
- [ ] **Database Connection Interface**:
  - [ ] Neo4j connection form (host, port, credentials)
  - [ ] Relational DB connection form (multiple DB types)
  - [ ] Connection testing and validation
  - [ ] Saved connection management
- [ ] **Streaming Configuration Interface**:
  - [ ] Kafka topic subscription setup
  - [ ] Vendor API integration forms
  - [ ] Real-time data preview
- [ ] **Demo Mode Features** (no key required):
  - [ ] Sample dataset browser (read-only)
  - [ ] Pre-loaded demo graphs
  - [ ] Limited feature access UI indicators
- [ ] **Licensed Mode Features** (key required):
  - [ ] Full data input capabilities
  - [ ] Dataset list/grid view with account isolation
  - [ ] Dataset metadata editing
  - [ ] Dataset versioning and history
  - [ ] Dataset deletion with confirmation
  - [ ] Data export to multiple formats

#### Milestone 4.2: Data Filtering & Selection

- [ ] Build trust score slider component
- [ ] Create feature selection dropdowns
- [ ] Implement multi-select for items
- [ ] Add real-time data preview
- [ ] Create filter preset saving
- [ ] Build advanced filter builder
- [ ] Add filter validation
- [ ] Implement filter state persistence

#### Milestone 4.3: Data Table View

- [ ] Create virtualized data table component
- [ ] Add sorting and pagination
- [ ] Implement column selection and reordering
- [ ] Add search and filtering within table
- [ ] Create export functionality (CSV, JSON, Excel)
- [ ] Add row selection and bulk actions
- [ ] Implement responsive table design

---

### **Phase 5: Network Visualization** (Weeks 10-12)

#### Milestone 5.1: Interactive Network Graph (react-force-graph)

- [ ] **2D Visualization (react-force-graph-2d)**:
  - [ ] Integrate react-force-graph-2d component
  - [ ] Configure force simulation parameters (charge, link distance)
  - [ ] Implement node styling based on attributes (size, color, shape)
  - [ ] Implement edge styling (width, color, dashed for weak ties)
  - [ ] Add zoom, pan, and drag interactions
  - [ ] Create node click/hover tooltips
  - [ ] Implement node selection and highlighting
  - [ ] Add path highlighting feature
  - [ ] Directed/undirected edge rendering
- [ ] **3D Visualization (react-force-graph-3d)**:
  - [ ] Integrate react-force-graph-3d component
  - [ ] 3D camera controls (orbit, zoom, pan)
  - [ ] 3D node and edge rendering
  - [ ] Performance optimization for 3D rendering
  - [ ] 2D/3D view toggle
- [ ] **Performance Optimization**:
  - [ ] WebGL acceleration
  - [ ] Level-of-detail (LOD) rendering
  - [ ] Graph simplification for large datasets (10K+ nodes)
  - [ ] Lazy loading for graph sections
  - [ ] Worker thread for force calculations
- [ ] **Demo vs Licensed Features**:
  - [ ] Demo: Limited to 100 nodes, watermark
  - [ ] Licensed: Full graph rendering, no limits

#### Milestone 5.2: Graph Controls & Configuration

- [ ] Create physics simulation controls
- [ ] Build layout algorithm selector (force, hierarchical, circular)
- [ ] Add node sizing options
- [ ] Implement edge weight visualization
- [ ] Create color scheme selector
- [ ] Add label visibility controls
- [ ] Implement graph filtering within visualization
- [ ] Create full-screen mode

#### Milestone 5.3: Graph Analytics Panel

- [ ] Display real-time graph metrics
- [ ] Create metrics visualization:
  - [ ] Nodes and edges count
  - [ ] Network density gauge
  - [ ] Clustering coefficient chart
  - [ ] Efficiency score
- [ ] Show top cliques
- [ ] Display connection recommendations
- [ ] Add exportable analytics report
- [ ] Create comparison view for different filters

---

### **Phase 6: Advanced Visualizations** (Weeks 13-15)

#### Milestone 6.1: Sankey Diagram

- [ ] Integrate React-Flow or D3 Sankey
- [ ] Build relationship flow visualization
- [ ] Add interactive node hover details
- [ ] Implement flow value encoding
- [ ] Create relationship count table
- [ ] Add export functionality (PNG, SVG)
- [ ] Optimize for performance

#### Milestone 6.2: Time Series Analysis

- [ ] Build time series chart components
- [ ] Create monthly activity visualization
- [ ] Add day-of-week heatmap
- [ ] Implement hourly activity chart
- [ ] Add date range selector
- [ ] Create time-based filtering
- [ ] Implement animation/playback feature
- [ ] Add trend analysis overlay

#### Milestone 6.3: Additional Visualizations

- [ ] Create correlation matrix heatmap
- [ ] Build hierarchical tree view
- [ ] Add community detection visualization
- [ ] Implement centrality measures charts
- [ ] Create comparative analysis views
- [ ] Add custom dashboard builder

---

### **Phase 7: Advanced Features** (Weeks 16-18)

#### Milestone 7.1: Vendor Streaming & Batch Integration

- [ ] **Kafka Integration**:
  - [ ] Kafka cluster setup and configuration
  - [ ] Consumer group management per tenant
  - [ ] Schema registry for data validation
  - [ ] Dead letter queue for failed messages
- [ ] **Vendor API Connectors** (modular design):
  - [ ] REST API polling module
  - [ ] Webhook receiver module
  - [ ] OAuth integration for vendor auth
  - [ ] Rate limiting and retry logic
- [ ] **Batch Processing Pipeline**:
  - [ ] Scheduled batch job runner
  - [ ] Large file processing (parallel chunks)
  - [ ] Data validation and error reporting
  - [ ] Progress tracking and notifications
- [ ] **Real-time Data Updates**:
  - [ ] WebSocket for live graph updates
  - [ ] Incremental graph refresh
  - [ ] Change notifications to frontend
- [ ] **Monitoring & Alerts**:
  - [ ] Data ingestion metrics dashboard
  - [ ] Error tracking and alerting
  - [ ] Vendor connection health checks

#### Milestone 7.2: Real-time Collaboration

- [ ] Implement WebSocket connection
- [ ] Add multi-user session support
- [ ] Create live cursor tracking
- [ ] Build collaborative filtering
- [ ] Add comment and annotation system
- [ ] Implement change notifications
- [ ] Create activity feed

#### Milestone 7.3: Reports & Export

- [ ] Design report templates
- [ ] Build PDF report generation
- [ ] Create PowerPoint export
- [ ] Add scheduled report generation
- [ ] Implement email delivery
- [ ] Create report customization UI
- [ ] Add report history and versioning

#### Milestone 7.4: Admin Panel & License Management

- [ ] Create user management interface
- [ ] Build role-based access control (RBAC)
- [ ] Add system settings configuration
- [ ] Implement usage analytics dashboard
- [ ] Create audit log viewer
- [ ] Add system health monitoring
- [ ] Build data retention policies

---

### **Phase 8: Performance & Optimization** (Weeks 19-20)

#### Milestone 8.1: Frontend Optimization

- [ ] Implement code splitting and lazy loading
- [ ] Optimize bundle size (< 200KB initial)
- [ ] Add service worker for offline support
- [ ] Implement Progressive Web App (PWA) features
- [ ] Optimize image and asset loading
- [ ] Add performance monitoring (Lighthouse CI)
- [ ] Implement virtual scrolling for large lists

#### Milestone 8.2: Backend Optimization

- [ ] Profile and optimize database queries
- [ ] Implement query result caching
- [ ] Add database connection pooling
- [ ] Optimize graph algorithms
- [ ] Implement horizontal scaling strategy
- [ ] Add request compression
- [ ] Create database indexes for common queries
- [ ] Optimize file upload handling

#### Milestone 8.3: Infrastructure Optimization

- [ ] Set up CDN for static assets
- [ ] Implement load balancing
- [ ] Add auto-scaling configuration
- [ ] Optimize Docker images (multi-stage builds)
- [ ] Set up database replication
- [ ] Implement backup and disaster recovery
- [ ] Add monitoring and alerting (Prometheus/Grafana)

---

### **Phase 9: Testing & Quality Assurance** (Weeks 21-22)

#### Milestone 9.1: Frontend Testing

- [ ] Unit tests for components (80%+ coverage)
- [ ] Integration tests for Redux slices
- [ ] E2E tests with Playwright/Cypress:
  - [ ] User authentication flow
  - [ ] Dataset upload and management
  - [ ] Network visualization interaction
  - [ ] Report generation
- [ ] Accessibility testing (WCAG 2.1 AA)
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] Performance testing

#### Milestone 9.2: Backend Testing

- [ ] Unit tests for services (85%+ coverage)
- [ ] Integration tests for API endpoints
- [ ] Load testing (Apache JMeter/Locust)
- [ ] Security testing (OWASP Top 10)
- [ ] API contract testing
- [ ] Database migration testing
- [ ] Disaster recovery testing

#### Milestone 9.3: User Acceptance Testing

- [ ] Create UAT test scenarios
- [ ] Conduct stakeholder demos
- [ ] Gather and document feedback
- [ ] Create bug tracking system
- [ ] Prioritize and fix critical issues
- [ ] Conduct final regression testing

---

### **Phase 10: Deployment & Launch** (Weeks 23-24)

#### Milestone 10.1: Production Environment Setup

- [ ] Configure production Kubernetes cluster
- [ ] Set up production databases with backups
- [ ] Configure SSL certificates
- [ ] Set up domain and DNS
- [ ] Implement production logging
- [ ] Configure monitoring and alerting
- [ ] Create deployment runbooks

#### Milestone 10.2: Security Hardening

- [ ] Security audit and penetration testing
- [ ] Implement rate limiting and DDoS protection
- [ ] Configure Web Application Firewall (WAF)
- [ ] Set up intrusion detection
- [ ] Implement data encryption at rest
- [ ] Configure secure API keys management
- [ ] Create security incident response plan

#### Milestone 10.3: Launch Preparation

- [ ] Create user documentation
- [ ] Build onboarding tutorials
- [ ] Prepare marketing materials
- [ ] Set up customer support channels
- [ ] Create training materials
- [ ] Develop migration plan from old system
- [ ] Conduct soft launch with beta users

#### Milestone 10.4: Go-Live

- [ ] Execute production deployment
- [ ] Monitor system performance
- [ ] Conduct post-launch health checks
- [ ] Enable production monitoring and alerting
- [ ] Activate customer support
- [ ] Publish release notes
- [ ] Celebrate! 🎉

---

## Post-Launch Roadmap (Months 7-12)

### Phase 11: Enhancements & Maintenance

- [ ] Gather user feedback and analytics
- [ ] Implement feature requests based on priority
- [ ] Regular security updates and patches
- [ ] Performance optimization based on usage patterns
- [ ] Scale infrastructure as needed
- [ ] Implement advanced ML features:
  - [ ] Anomaly detection in networks
  - [ ] Predictive analytics
  - [ ] Automated insights generation
- [ ] Mobile native apps (React Native)
- [ ] API marketplace for third-party integrations

---

## Project Timeline

| Phase                               | Duration     | Weeks         |
| ----------------------------------- | ------------ | ------------- |
| Phase 1: Foundation & Setup         | 2 weeks      | 1-2           |
| Phase 2: Core Backend Services      | 3 weeks      | 3-5           |
| Phase 3: Frontend Foundation        | 3 weeks      | 4-6           |
| Phase 4: Data Management            | 3 weeks      | 7-9           |
| Phase 5: Network Visualization      | 3 weeks      | 10-12         |
| Phase 6: Advanced Visualizations    | 3 weeks      | 13-15         |
| Phase 7: Advanced Features          | 3 weeks      | 16-18         |
| Phase 8: Performance & Optimization | 2 weeks      | 19-20         |
| Phase 9: Testing & QA               | 2 weeks      | 21-22         |
| Phase 10: Deployment & Launch       | 2 weeks      | 23-24         |
| **Total**                           | **24 weeks** | **~6 months** |

---

## Team Structure (Recommended)

### Core Team

- **1x Tech Lead / Architect** - Overall architecture and technical decisions
- **2x Senior Full-Stack Developers** - React + Python
- **1x Frontend Developer** - React/TypeScript specialist
- **1x Backend Developer** - Python/FastAPI specialist
- **1x DevOps Engineer** - Infrastructure and CI/CD
- **1x UI/UX Designer** - Design system and user experience
- **1x QA Engineer** - Testing and quality assurance
- **1x Product Manager** - Requirements and stakeholder management

### Extended Team (Part-time)

- Data Scientist - Algorithm optimization
- Security Specialist - Security audit
- Technical Writer - Documentation

---

## Risk Management

### Technical Risks

| Risk                                 | Impact   | Mitigation                                             |
| ------------------------------------ | -------- | ------------------------------------------------------ |
| Performance issues with large graphs | High     | Implement virtualization, server-side rendering, WebGL |
| Data security concerns               | Critical | End-to-end encryption, regular audits, compliance      |
| Scalability bottlenecks              | High     | Horizontal scaling, caching, CDN, load balancing       |
| Third-party library vulnerabilities  | Medium   | Regular dependency updates, security scanning          |
| Browser compatibility                | Medium   | Polyfills, progressive enhancement, testing            |

### Project Risks

| Risk                  | Impact | Mitigation                                         |
| --------------------- | ------ | -------------------------------------------------- |
| Scope creep           | High   | Strict change management, agile sprints            |
| Resource availability | High   | Cross-training, documentation, knowledge sharing   |
| Timeline delays       | Medium | Buffer time, MVP approach, parallel development    |
| Stakeholder alignment | Medium | Regular demos, clear communication, feedback loops |

---

## Success Metrics

### Technical KPIs

- **Performance**: Page load < 2s, Time to Interactive < 3s
- **Reliability**: 99.9% uptime
- **Scalability**: Support 10,000+ concurrent users
- **Code Quality**: 80%+ test coverage, < 5% bug rate
- **Security**: Zero critical vulnerabilities

### Business KPIs

- **User Adoption**: 80% of current Streamlit users migrate
- **User Satisfaction**: NPS > 50
- **Performance**: 50% faster than current system
- **Feature Usage**: 70% of users use advanced features
- **Support Tickets**: < 5% of users need support

---

## Budget Estimate (High-Level)

### Development Costs (6 months)

- Team salaries: $400,000 - $600,000
- Infrastructure (dev/staging/prod): $5,000 - $10,000
- Third-party services and APIs: $2,000 - $5,000
- Tools and licenses: $3,000 - $5,000
- **Total Development**: ~$410,000 - $620,000

### Ongoing Costs (Annual)

- Infrastructure and hosting: $30,000 - $60,000 (includes Neo4j cluster, Kafka)
- Maintenance and support: $100,000 - $150,000
- Monitoring and observability: $5,000 - $10,000
- Security and compliance: $10,000 - $20,000
- Neo4j Enterprise license: $15,000 - $30,000 (if using Enterprise)
- **Total Annual**: ~$160,000 - $270,000

---

## Technology Decision Rationale

### Why React.js?

- Industry standard with massive ecosystem
- Component reusability and maintainability
- Strong TypeScript support
- Excellent visualization library support
- Large talent pool

### Why react-force-graph-2d/3d?

- **WebGL-accelerated** rendering for high performance (10K+ nodes)
- Built on Three.js/D3.js for robust graph visualization
- Native support for force-directed layouts
- Easy customization of node/edge appearance
- Seamless 2D/3D switching
- Active maintenance and community support
- Better performance than DOM-based solutions (Vis.js, Cytoscape.js)

### Why FastAPI (Python Backend with Modules)?

- Leverages existing Python data science stack
- High performance (async/await)
- Automatic API documentation
- Strong typing with Pydantic
- Easy integration with NetworkX, Pandas
- **Module-based architecture**: simpler than classes, easier to test and maintain
- Functional programming paradigm fits data processing workflows

### Why Neo4j?

- **Native graph database** - optimized for graph traversals
- Cypher query language - intuitive and powerful
- Built-in graph algorithms library
- Excellent multi-tenancy support with labels/namespaces
- Horizontal scaling with clustering
- Superior performance for complex graph queries vs. relational DBs
- Industry standard for graph data

### Why Microservices?

- Independent scaling of compute-intensive services
- Better fault isolation
- Technology flexibility per service
- Easier maintenance and updates
- Supports multiple data source connectors

### Why Multi-Database Strategy?

- **Neo4j**: Native graph storage and queries, multi-tenant isolation
- **PostgreSQL**: Relational data (licenses, accounts), ACID compliance
- **MongoDB**: Fast document queries for preprocessed graph data
- **Redis**: Sub-millisecond caching, rate limiting, session management
- Each database optimized for its use case

### Why Apache Kafka?

- **High-throughput** streaming data ingestion
- Durable message storage (replay capability)
- Horizontal scalability
- Built-in partitioning for multi-tenant isolation
- Industry standard for real-time data pipelines
- Support for exactly-once semantics

### Why API Key-based Licensing?

- **Simpler than OAuth** for B2B SaaS model
- Easy integration for customers
- Fine-grained feature control by tier
- Lower implementation complexity
- Better for demo/trial conversions
- Standard for API-driven products

---

## Python Module-Based Architecture Pattern

### Design Principles (No Classes)

The backend will follow a **functional, module-based architecture** instead of object-oriented class-based design:

```python
# ❌ AVOID: Class-based approach
class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def calculate_metrics(self):
        return self._internal_method()

# ✅ PREFER: Module-based functional approach
def calculate_graph_metrics(graph: nx.Graph) -> dict:
    """Calculate network metrics for a graph."""
    return {
        'density': nx.density(graph),
        'clustering': nx.average_clustering(graph),
        'nodes': graph.number_of_nodes()
    }
```

### Module Organization

```
backend/
├── api/
│   ├── gateway.py              # FastAPI app initialization
│   ├── routes/
│   │   ├── license_routes.py   # License validation endpoints
│   │   ├── data_routes.py      # Data ingestion endpoints
│   │   ├── graph_routes.py     # Graph analytics endpoints
│   │   └── export_routes.py    # Export and reporting endpoints
│   └── middleware/
│       ├── auth_middleware.py  # API key validation functions
│       └── tenant_middleware.py # Multi-tenant isolation
├── services/
│   ├── ingestion/
│   │   ├── neo4j_connector.py  # Neo4j connection and query functions
│   │   ├── sql_connector.py    # Relational DB connectors
│   │   ├── file_parser.py      # Edge file parsing functions
│   │   ├── kafka_consumer.py   # Streaming data consumer
│   │   └── batch_processor.py  # Batch upload handler
│   ├── processing/
│   │   ├── data_transformer.py # Data transformation functions
│   │   ├── graph_builder.py    # NetworkX graph construction
│   │   └── data_validator.py   # Validation functions
│   ├── analytics/
│   │   ├── metrics_calculator.py    # Basic metrics (density, clustering)
│   │   ├── centrality_analyzer.py   # Centrality measures
│   │   ├── community_detector.py    # Community detection
│   │   ├── clique_finder.py         # Maximal cliques
│   │   └── path_analyzer.py         # Shortest paths, recommendations
│   ├── visualization/
│   │   ├── graph_preprocessor.py    # Prepare data for react-force-graph
│   │   └── layout_calculator.py     # Pre-compute layouts
│   └── licensing/
│       ├── key_generator.py    # License key generation
│       ├── key_validator.py    # Key validation logic
│       └── feature_gates.py    # Feature availability by tier
├── database/
│   ├── neo4j_ops.py            # Neo4j CRUD operations
│   ├── postgres_ops.py         # PostgreSQL operations (no ORM)
│   ├── mongo_ops.py            # MongoDB operations
│   └── redis_ops.py            # Redis caching functions
├── models/
│   ├── graph_schema.py         # Pydantic models for graph data
│   ├── license_schema.py       # License tier definitions
│   └── tenant_schema.py        # Tenant/account models
└── utils/
    ├── logging_utils.py        # Logging helpers
    ├── error_handlers.py       # Error handling functions
    └── config.py               # Configuration management
```

### Example Module Patterns

#### Neo4j Connector Module

```python
# services/ingestion/neo4j_connector.py
from neo4j import GraphDatabase
from typing import List, Dict, Any

def create_connection(uri: str, user: str, password: str):
    """Create Neo4j driver connection."""
    return GraphDatabase.driver(uri, auth=(user, password))

def fetch_graph_by_tenant(driver, tenant_id: str, filters: dict) -> List[Dict[str, Any]]:
    """Fetch graph data for a specific tenant."""
    with driver.session() as session:
        query = """
        MATCH (n:Node {tenant_id: $tenant_id})-[r:EDGE]->(m:Node)
        WHERE r.weight >= $min_weight
        RETURN n, r, m
        """
        result = session.run(query, tenant_id=tenant_id, **filters)
        return [record.data() for record in result]

def write_graph_to_neo4j(driver, tenant_id: str, edges: List[Dict]) -> int:
    """Write graph edges to Neo4j with tenant isolation."""
    with driver.session() as session:
        query = """
        UNWIND $edges as edge
        MERGE (n:Node {id: edge.source, tenant_id: $tenant_id})
        MERGE (m:Node {id: edge.target, tenant_id: $tenant_id})
        MERGE (n)-[r:EDGE {tenant_id: $tenant_id}]->(m)
        SET r.weight = edge.weight
        """
        result = session.run(query, edges=edges, tenant_id=tenant_id)
        return result.consume().counters.relationships_created
```

#### Graph Analytics Module

```python
# services/analytics/metrics_calculator.py
import networkx as nx
from typing import Dict, Any

def calculate_basic_metrics(graph: nx.Graph) -> Dict[str, Any]:
    """Calculate basic network metrics."""
    return {
        'nodes': graph.number_of_nodes(),
        'edges': graph.number_of_edges(),
        'density': nx.density(graph),
        'avg_clustering': nx.average_clustering(graph),
        'transitivity': nx.transitivity(graph)
    }

def calculate_efficiency(graph: nx.Graph) -> float:
    """Calculate global efficiency of the network."""
    return nx.global_efficiency(graph)

def find_connected_components(graph: nx.Graph) -> List[set]:
    """Find all connected components."""
    return list(nx.connected_components(graph))
```

#### License Validation Module

```python
# services/licensing/key_validator.py
from typing import Optional, Dict
from datetime import datetime
import hashlib

def validate_license_key(key: str, db_conn) -> Optional[Dict]:
    """Validate license key and return tier information."""
    # Query license from database
    license_info = db_conn.query_license(key_hash=hashlib.sha256(key.encode()).hexdigest())

    if not license_info:
        return None

    if license_info['expires_at'] < datetime.utcnow():
        return None

    return {
        'tier': license_info['tier'],
        'features': get_features_for_tier(license_info['tier']),
        'account_id': license_info['account_id']
    }

def get_features_for_tier(tier: str) -> Dict[str, bool]:
    """Return feature availability for license tier."""
    features = {
        'demo': {
            'data_input': False,
            'max_nodes': 100,
            'export': False,
            'streaming': False,
            '3d_visualization': False
        },
        'basic': {
            'data_input': True,
            'max_nodes': 5000,
            'export': True,
            'streaming': False,
            '3d_visualization': True
        },
        'professional': {
            'data_input': True,
            'max_nodes': 50000,
            'export': True,
            'streaming': True,
            '3d_visualization': True
        },
        'enterprise': {
            'data_input': True,
            'max_nodes': None,  # unlimited
            'export': True,
            'streaming': True,
            '3d_visualization': True
        }
    }
    return features.get(tier, features['demo'])
```

### Benefits of Module-Based Approach

1. **Simplicity**: Easier to understand and reason about
2. **Testability**: Pure functions are easier to unit test
3. **Composability**: Functions can be easily combined
4. **No State Management**: Eliminates hidden state bugs
5. **Parallel Processing**: Stateless functions work well with async/multiprocessing
6. **Documentation**: Function signatures are self-documenting
7. **Refactoring**: Easier to move and reorganize code

---

## License Tier Feature Matrix

| Feature                  | Demo (No Key)      | Basic         | Professional   | Enterprise      |
| ------------------------ | ------------------ | ------------- | -------------- | --------------- |
| **Data Input**           |
| Sample datasets          | ✅ Read-only       | ✅            | ✅             | ✅              |
| CSV/JSON upload          | ❌                 | ✅ (500 MB)   | ✅ (5 GB)      | ✅ Unlimited    |
| Neo4j connection         | ❌                 | ✅            | ✅             | ✅              |
| Relational DB connection | ❌                 | ❌            | ✅             | ✅              |
| Streaming (Kafka)        | ❌                 | ❌            | ✅             | ✅              |
| **Visualization**        |
| 2D network graph         | ✅ (100 nodes max) | ✅ (5K nodes) | ✅ (50K nodes) | ✅ Unlimited    |
| 3D network graph         | ❌                 | ✅            | ✅             | ✅              |
| Time series              | ✅ Basic           | ✅            | ✅             | ✅              |
| Sankey diagrams          | ✅                 | ✅            | ✅             | ✅              |
| **Analytics**            |
| Basic metrics            | ✅                 | ✅            | ✅             | ✅              |
| Centrality measures      | ❌                 | ✅            | ✅             | ✅              |
| Community detection      | ❌                 | ❌            | ✅             | ✅              |
| Path analysis            | ❌                 | ✅ Limited    | ✅             | ✅              |
| **Export & Sharing**     |
| Export graph (PNG)       | ❌                 | ✅            | ✅             | ✅              |
| Export data (CSV)        | ❌                 | ✅            | ✅             | ✅              |
| PDF reports              | ❌                 | ❌            | ✅             | ✅              |
| API access               | ❌                 | Read-only     | Full           | Full + webhooks |
| **Collaboration**        |
| Users per account        | 1                  | 5             | 25             | Unlimited       |
| Real-time collaboration  | ❌                 | ❌            | ✅             | ✅              |
| **Storage & Limits**     |
| Data storage             | N/A                | 10 GB         | 100 GB         | Unlimited       |
| API calls/month          | 100                | 10,000        | 100,000        | Unlimited       |
| **Support**              |
| Support                  | Community          | Email         | Priority email | 24/7 + phone    |
| **Pricing**              | Free               | $99/mo        | $499/mo        | Custom          |

---

## Next Steps

1. **Stakeholder Review** - Review and approve this plan
2. **Team Assembly** - Recruit or assign team members
3. **Environment Setup** - Provision development infrastructure
4. **Sprint 0** - Project kickoff, tool setup, initial architecture
5. **Begin Phase 1** - Start foundation and setup work

---

## Document Control

| Version | Date       | Author         | Changes                                                                                                                                                                                       |
| ------- | ---------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-01-06 | GitHub Copilot | Initial development plan                                                                                                                                                                      |
| 2.0     | 2026-01-06 | GitHub Copilot | Updated architecture: Neo4j graph DB, multi-source data ingestion (streaming/batch), react-force-graph-2d/3d, Python modules only (no classes), API key-based licensing with demo/tier system |

---

**Document Status**: Draft v2.0  
**Last Updated**: January 6, 2026  
**Next Review**: January 20, 2026
