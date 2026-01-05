# Contributing to ONA Platform v2.0

Thank you for your interest in contributing to the ONA Platform! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/New-ONA.git
   cd New-ONA
   ```
3. **Set up development environment**: Follow [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## Development Process

### Architecture Guidelines

- Review [ARCHITECTURE_SUMMARY.md](./ARCHITECTURE_SUMMARY.md) for design patterns
- Follow [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for project phases
- Check [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for file organization

### Python Backend Rules

**CRITICAL: No Classes - Modules Only**

✅ **DO: Use functional modules**

```python
# ✅ services/analytics/metrics_calculator.py
def calculate_density(graph: nx.Graph) -> float:
    """Calculate network density."""
    return nx.density(graph)

def calculate_clustering(graph: nx.Graph) -> float:
    """Calculate average clustering coefficient."""
    return nx.average_clustering(graph)
```

❌ **DON'T: Use classes**

```python
# ❌ Avoid this pattern
class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph
```

### Frontend Standards

- Use **TypeScript** (not JavaScript)
- Functional components with hooks (no class components)
- Follow **Material-UI** design system
- Use **react-force-graph-2d/3d** for network visualization

---

## Coding Standards

### Python (Backend)

- **Style**: PEP 8 compliant
- **Formatting**: Use `black` formatter
- **Linting**: Use `pylint` and `mypy`
- **Type hints**: Required for all functions
- **Docstrings**: Google style docstrings

```python
def calculate_metrics(graph: nx.Graph) -> Dict[str, float]:
    """
    Calculate basic network metrics.

    Args:
        graph: NetworkX graph instance

    Returns:
        Dictionary of metric name to value

    Raises:
        ValueError: If graph is empty
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph cannot be empty")

    return {
        "density": nx.density(graph),
        "clustering": nx.average_clustering(graph)
    }
```

### TypeScript (Frontend)

- **Style**: Follow Airbnb style guide
- **Formatting**: Use Prettier
- **Linting**: Use ESLint
- **Types**: Avoid `any`, use proper types

```typescript
interface GraphData {
  nodes: Node[];
  edges: Edge[];
}

const calculateNodeSize = (node: Node): number => {
  return Math.sqrt(node.degree) * 5;
};
```

### Testing

- **Coverage**: Minimum 80% for new code
- **Unit tests**: For all functions
- **Integration tests**: For API endpoints
- **E2E tests**: For critical user flows

---

## Submitting Changes

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(analytics): add community detection algorithm

Implements Louvain community detection for Professional tier users.
Uses NetworkX library for efficient computation.

Closes #123
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Run tests locally**:

   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend
   npm test
   ```

4. **Update CHANGELOG.md** (if applicable)
5. **Create pull request** with clear description
6. **Request review** from maintainers
7. **Address feedback** promptly

### PR Checklist

- [ ] Code follows module-based pattern (no classes)
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No new linting errors
- [ ] Self-reviewed code
- [ ] Comments added for complex logic

---

## Reporting Bugs

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)

Include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (license tier, browser, OS)
- Screenshots if applicable
- Error messages

---

## Feature Requests

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)

Include:

- Problem description
- Proposed solution
- Use case
- License tier consideration
- Priority level

---

## Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Test additions

**Examples:**

- `feature/kafka-streaming`
- `fix/neo4j-connection-pool`
- `docs/scalability-guide`

---

## Testing Guidelines

### Backend Tests

```python
# tests/unit/test_metrics_calculator.py
import pytest
import networkx as nx
from services.analytics.metrics_calculator import calculate_density

def test_calculate_density_empty_graph():
    """Test density calculation on empty graph."""
    graph = nx.Graph()
    with pytest.raises(ValueError):
        calculate_density(graph)

def test_calculate_density_complete_graph():
    """Test density of complete graph should be 1.0."""
    graph = nx.complete_graph(5)
    assert calculate_density(graph) == 1.0
```

### Frontend Tests

```typescript
// ForceGraph2D.test.tsx
import { render, screen } from "@testing-library/react";
import { ForceGraph2DComponent } from "./ForceGraph2D";

describe("ForceGraph2D", () => {
  it("renders graph with nodes", () => {
    const data = {
      nodes: [{ id: "1" }, { id: "2" }],
      edges: [{ source: "1", target: "2" }],
    };

    render(<ForceGraph2DComponent data={data} />);
    // Add assertions
  });
});
```

---

## Documentation

- Update relevant .md files in docs/ directory
- Add code examples for new features
- Update API documentation
- Include diagrams if helpful

---

## Questions?

- Check [INDEX.md](./INDEX.md) for navigation
- Review [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- Open a discussion on GitHub
- Contact maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to ONA Platform!** 🎉
