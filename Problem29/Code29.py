from collections import defaultdict

def find_unexplored_edge(graph, visited_edges, node):
    """Find an unexplored edge from the given node."""
    for neighbor in graph[node]:
        if (node, neighbor) not in visited_edges:
            return neighbor
    return None

def eulerian_cycle(graph):
    """Find an Eulerian cycle in the directed graph."""
    # Convert graph to list of edges format and count total edges
    total_edges = sum(len(neighbors) for neighbors in graph.values())

    # Initialize visited edges set
    visited_edges = set()

    # Start from any node (we'll use the first node in the graph)
    start = list(graph.keys())[0]
    cycle = [start]
    current = start

    # Form initial cycle
    while True:
        next_node = find_unexplored_edge(graph, visited_edges, current)
        if next_node is None:
            break
        visited_edges.add((current, next_node))
        cycle.append(next_node)
        current = next_node

    # While there are unexplored edges
    while len(visited_edges) < total_edges:
        # Find a node in cycle with unexplored edges
        new_start = None
        for i, node in enumerate(cycle):
            if find_unexplored_edge(graph, visited_edges, node) is not None:
                new_start = i
                break

        # Form new cycle starting from new_start
        new_cycle = cycle[new_start:]
        new_cycle.extend(cycle[1:new_start + 1])
        cycle = new_cycle

        # Add the random walk part
        current = cycle[-1]
        while True:
            next_node = find_unexplored_edge(graph, visited_edges, current)
            if next_node is None:
                break
            visited_edges.add((current, next_node))
            cycle.append(next_node)
            current = next_node

    return cycle

def has_eulerian_cycle(graph):
    """Check if the graph has an Eulerian cycle."""
    # Convert the graph to calculate in-degrees
    in_degree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Check if in-degree equals out-degree for each node
    for node in graph:
        if len(graph[node]) != in_degree[node]:
            return False
    return True

# Example usage
if __name__ == "__main__":
    # Example graph
    graph = {
        0: [3],
        1: [0],
        2: [1, 6],
        3: [2],
        4: [2],
        5: [4],
        6: [5, 8],
        7: [9],
        8: [7],
        9: [6]
    }

    if has_eulerian_cycle(graph):
        cycle = eulerian_cycle(graph)
        print("Eulerian cycle:", " -> ".join(map(str, cycle)))
    else:
        print("The graph does not contain an Eulerian cycle")
