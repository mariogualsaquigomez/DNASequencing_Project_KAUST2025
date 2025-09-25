class Node:
    def __init__(self, value):
        self.value = value  # Unique identifier or data for the node
        self.neighbors = [] # List to store references to neighboring Node objects

    def add_neighbor(self, neighbor_node):
        #if neighbor_node not in self.neighbors: #For unique Nodes
            #self.neighbors.append(neighbor_node)
        self.neighbors.append(neighbor_node)

    def __repr__(self):
        return f"{self.value}"

class Graph:
    def __init__(self):
        self.nodes = {} # Dictionary to store Node objects, keyed by their value

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
        #node2.add_neighbor(node1) # For an undirected graph

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
    #k = len(ListPatterns[0])
    for pattern in ListPatterns:
        Debruijn_graph.add_edge(pattern[:-1], pattern[1:])
    return Debruijn_graph

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

def eulerian_path(graph):
    if not graph:
        return None

    # Calculate in-degrees and out-degrees for all vertices
    in_degree = {}
    out_degree = {}

    # Initialize degrees
    for u in graph:
        out_degree[u] = len(graph[u])
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
            # Also ensure vertices with only incoming edges are in in_degree
            if v not in out_degree:
                out_degree[v] = 0
        # Ensure vertices with only outgoing edges are in in_degree
        if u not in in_degree:
            in_degree[u] = 0

    # Find start vertex (vertex with out_degree = in_degree + 1)
    # If no such vertex exists, try to find a vertex with out_degree > 0
    start = None
    for v in out_degree:
        if out_degree[v] - in_degree.get(v, 0) == 1:
            start = v
            break
    if start is None:
        # If no vertex with out_degree = in_degree + 1, take any vertex with edges
        for v in out_degree:
            if out_degree[v] > 0:
                start = v
                break

    if start is None:
        return None  # No valid start vertex found

    # Hierholzer's algorithm to find Eulerian path
    path = []
    stack = [start]
    current_path = []

    while stack:
        current = stack[-1]
        if out_degree[current] == 0:
            # If no more outgoing edges, add to path
            current_path.append(stack.pop())
        else:
            # Take next available edge
            next_vertex = graph[current][out_degree[current] - 1]
            out_degree[current] -= 1
            stack.append(next_vertex)

    # Reverse path to get correct order
    path = current_path[::-1]

    # Verify that we used all edges
    total_edges = sum(len(edges) for edges in graph.values())
    if len(path) - 1 != total_edges:
        return None

    return path