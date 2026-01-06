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
    filters: Optional[Dict[str, Any]] = None,
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
            limit=filters.get("limit", 10000),
        )

        return [
            {
                "source": record["source_id"],
                "target": record["target_id"],
                "weight": record["weight"],
                "edge_properties": record["edge_props"],
                "source_properties": record["source_props"],
                "target_properties": record["target_props"],
            }
            for record in result
        ]


def write_graph_edges(
    driver: Driver,
    tenant_id: str,
    edges: List[Dict[str, Any]],
    node_label: str = "Node",
    edge_type: str = "EDGE",
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
            "properties_set": summary.counters.properties_set,
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
