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

def prefix(text):
    return text[:-1]

def suffix(text):
    return text[1:]

def PairedCompositeGraph(ListPairedPatterns, k):
    Debruijn_graph = Graph()
    # k = len(ListPatterns[0])
    for pattern in ListPairedPatterns:
        (seq1, seq2) = pattern.split("|")
        Debruijn_graph.add_edge("|".join([prefix(seq1),prefix(seq2)]), "|".join([suffix(seq1),suffix(seq2)]))
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

def glue_sequences(path, k, d):
    glued = ''
    seq1_array = []
    seq2_array = []
    for seq in path:
        seq1, seq2 = seq.split("|")
        seq1_array.append(seq1)
        seq2_array.append(seq2)
    for_seq = seq1_array[0] + "".join([x[-1] for x in seq1_array[1:]])
    rev_seq = "".join(x[0] for x in seq2_array[:-1]) + seq2_array[-1]
    comparison_seq = [int(a==b) for a, b in zip(for_seq[k+d:], rev_seq[:-k-d])]
    if sum(comparison_seq)== len(comparison_seq):
        glued += for_seq[:k+d] + rev_seq
    else:
        return "there is no string speeded by the gapped patterns"
    return glued

# Example usage
if __name__ == "__main__":
    # Example graph
    kmers = ['GACC|GCGC', 'ACCG|CGCC', 'CCGA|GCCG', 'CGAG|CCGG', 'GAGC|CGGA']
    k = 4
    d = 2
    graph_seq = PairedCompositeGraph(kmers, k)
    # We suppose all graphs and sequences received are strongly connected
    if has_eulerian_cycle_direct(graph_seq):
        cycle = eulerian_cycle_direct(graph_seq)
        print("Eulerian cycle:", " -> ".join(map(str, cycle)))
        print("Glued sequence:", glue_sequences(cycle, k, d))
    else:
        path = eulerian_path_direct(graph_seq)
        if path:
            print("Eulerian path:", " -> ".join(map(str, path)))
            print("Glued sequence:", glue_sequences(path, k, d))
        else:
            print("Neither Eulerian path nor Eulerian cycle was found.")