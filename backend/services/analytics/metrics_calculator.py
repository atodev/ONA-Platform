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
        "is_connected": nx.is_connected(graph),
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
        "eigenvector": dict(nx.eigenvector_centrality(graph, max_iter=1000)),
    }


def find_top_nodes_by_centrality(
    graph: nx.Graph, centrality_type: str = "degree", top_n: int = 10
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
        "eigenvector": nx.eigenvector_centrality,
    }

    if centrality_type not in centrality_funcs:
        raise ValueError(f"Unknown centrality type: {centrality_type}")

    centrality = centrality_funcs[centrality_type](graph)
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

    return [{"node": node, "score": score} for node, score in sorted_nodes[:top_n]]


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
    graph: nx.Graph, source: str, target: str
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

        return {"path": path, "length": length, "exists": True}
    except nx.NetworkXNoPath:
        return {"path": [], "length": float("inf"), "exists": False}
