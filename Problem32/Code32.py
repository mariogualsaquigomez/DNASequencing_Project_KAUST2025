from collections import defaultdict
import glob

class Node:
    def __init__(self, value):
        self.value = value  # Unique identifier or data for the node
        self.neighbors = []  # List to store references to neighboring Node objects

    def add_neighbor(self, neighbor_node):
        # if neighbor_node not in self.neighbors: #For unique Nodes
        # self.neighbors.append(neighbor_node)
        self.neighbors.append(neighbor_node)

    def __repr__(self):
        return f"{self.value}"

class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store Node objects, keyed by their value

    def add_node(self, value):
        if value not in self.nodes:
            new_node = Node(value)
            self.nodes[value] = new_node
            return new_node
        return self.nodes[value]

    def add_edge(self, value1, value2):
        node1 = self.add_node(value1)
        node2 = self.add_node(value2)
        node1.add_neighbor(node2)
        # node2.add_neighbor(node1) # For an undirected graph

    def get_node(self, value):
        return self.nodes.get(value)

    def sort_graph(self):
        self.nodes = dict(sorted(self.nodes.items()))
        return self.nodes

    def get_simplegraph(self):
        nodes = self.sort_graph()
        simplegraph = {}
        for node_value, node_obj in nodes.items():
            neighbor_values = sorted([n.value for n in node_obj.neighbors])
            if neighbor_values:
                simplegraph[node_value] = neighbor_values
        return simplegraph

    def __repr__(self):
        nodes = self.sort_graph()
        graph_repr = ""
        for node_value, node_obj in nodes.items():
            neighbor_values = sorted([n.value for n in node_obj.neighbors])
            if neighbor_values:
                graph_repr += f"{node_value} -> {",".join(neighbor_values)}\n"
        return graph_repr

def CompositeGraph(ListPatterns, k):
    Debruijn_graph = Graph()
    # k = len(ListPatterns[0])
    for pattern in ListPatterns:
        Debruijn_graph.add_edge(pattern[:-1], pattern[1:])
    return Debruijn_graph

def find_unexplored_edge_direct(node, visited_edges):
    """Find an unexplored edge from the given node using direct Graph object."""
    for neighbor in node.neighbors:
        if (node.value, neighbor.value) not in visited_edges:
            return neighbor
    return None

def eulerian_cycle_direct(graph):
    """Find an Eulerian cycle in the directed graph using Graph object."""
    # Count total edges
    total_edges = sum(len(node.neighbors) for node in graph.nodes.values())

    # Initialize visited edges set
    visited_edges = set()

    # Start from any node
    start_node = next(iter(graph.nodes.values()))
    cycle = [start_node]
    current = start_node

    # Form initial cycle
    while True:
        next_node = find_unexplored_edge_direct(current, visited_edges)
        if next_node is None:
            break
        visited_edges.add((current.value, next_node.value))
        cycle.append(next_node)
        current = next_node

    # While there are unexplored edges
    while len(visited_edges) < total_edges:
        # Find a node in cycle with unexplored edges
        new_start = None
        for i, node in enumerate(cycle):
            if find_unexplored_edge_direct(node, visited_edges) is not None:
                new_start = i
                break

        # Form new cycle starting from new_start
        new_cycle = cycle[new_start:]
        new_cycle.extend(cycle[1:new_start + 1])
        cycle = new_cycle

        # Add the random walk part
        current = cycle[-1]
        while True:
            next_node = find_unexplored_edge_direct(current, visited_edges)
            if next_node is None:
                break
            visited_edges.add((current.value, next_node.value))
            cycle.append(next_node)
            current = next_node

    return [node.value for node in cycle]

def has_eulerian_cycle_direct(graph):
    """Check if the Graph object has an Eulerian cycle."""
    # Calculate in-degrees
    in_degree = defaultdict(int)
    for node in graph.nodes.values():
        for neighbor in node.neighbors:
            in_degree[neighbor.value] += 1

    # Check if in-degree equals out-degree for each node
    for node in graph.nodes.values():
        if len(node.neighbors) != in_degree[node.value]:
            return False
    return True

def eulerian_path_direct(graph):
    """Find an Eulerian path in the directed Graph object."""
    if not graph.nodes:
        return None

    # Calculate in-degrees and out-degrees
    in_degree = defaultdict(int)
    out_degree = {}

    # Initialize degrees
    for node in graph.nodes.values():
        out_degree[node.value] = len(node.neighbors)
        for neighbor in node.neighbors:
            in_degree[neighbor.value] += 1
            if neighbor.value not in out_degree:
                out_degree[neighbor.value] = 0
        if node.value not in in_degree:
            in_degree[node.value] = 0

    # Find start vertex
    start = None
    for value, node in graph.nodes.items():
        if out_degree[value] - in_degree[value] == 1:
            start = node
            break
    if start is None:
        # If no vertex with out_degree = in_degree + 1, take any vertex with edges
        for value, node in graph.nodes.items():
            if out_degree[value] > 0:
                start = node
                break

    if start is None:
        return None

    # Hierholzer's algorithm
    path = []
    stack = [start]
    current_path = []

    remaining_edges = {node.value: list(node.neighbors) for node in graph.nodes.values()}

    while stack:
        current = stack[-1]
        if not remaining_edges[current.value]:
            current_path.append(stack.pop().value)
        else:
            next_vertex = remaining_edges[current.value].pop()
            stack.append(next_vertex)

    # Reverse path to get correct order
    path = current_path[::-1]

    # Verify that we used all edges
    total_edges = sum(len(node.neighbors) for node in graph.nodes.values())
    if len(path) - 1 != total_edges:
        return None

    return path

def generate_binary_kmers(k):
    """Generate all possible binary k-mers."""
    if k <= 0:
        return []

    kmers = []
    for i in range(2 ** k):
        # Convert number to binary and pad with zeros
        binary = format(i, f'0{k}b')
        kmers.append(binary)
    return kmers

def universal_circular_string(k):
    """
    Generate a k-universal circular binary string.
    The string contains all possible binary k-mers exactly once when read circularly.

    Args:
        k: Length of binary patterns to include

    Returns:
        A string that contains all binary k-mers when read circularly
    """
    if k <= 0:
        return ""

    # Generate all possible k-1 length binary patterns
    kmers = generate_binary_kmers(k - 1)

    # Create de Bruijn graph
    graph = Graph()

    # Add edges for all possible transitions
    for kmer in kmers:
        # For each k-1 mer, we can append either 0 or 1
        graph.add_edge(kmer, kmer[1:] + "0")
        graph.add_edge(kmer, kmer[1:] + "1")

    # Find Eulerian cycle
    cycle = eulerian_cycle_direct(graph)

    if not cycle:
        return None

    # Construct the universal string
    # We need only k-1 characters from each vertex except the first one
    result = cycle[0]
    for i in range(1, len(cycle)):
        result += cycle[i][-1]

    return result[:-k + 1]  # Remove last k-1 characters as they overlap with the beginning


# Usage:
if __name__ == "__main__":
    k = 9  # Change this value to generate different length universal strings
    result = universal_circular_string(k)
    if result:
        print(f"{result}")
        ##DEBUG CODE
        # print(f"{k}-universal circular binary string: {result}")
        # # Verify all k-mers are present
        # all_kmers = generate_binary_kmers(k)
        # # Make string circular by adding k-1 characters from the beginning
        # circular_string = result + result[:k - 1]
        # print("\nVerification - all binary {}-mers found in string:".format(k))
        # found_kmers = set()
        # for i in range(len(result)):
        #     kmer = circular_string[i:i + k]
        #     found_kmers.add(kmer)
        #
        # all_found = True
        # for kmer in all_kmers:
        #     present = kmer in found_kmers
        #     print(f"{kmer}: {'Found' if present else 'Not found'}")
        #     if not present:
        #         all_found = False
        #
        # print(f"\nAll {k}-mers present: {all_found}")

