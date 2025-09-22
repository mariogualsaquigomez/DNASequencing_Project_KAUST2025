class Node:
    def __init__(self, value):
        self.value = value  # Unique identifier or data for the node
        self.neighbors = [] # List to store references to neighboring Node objects

    def add_neighbor(self, neighbor_node):
        if neighbor_node not in self.neighbors:
            self.neighbors.append(neighbor_node)

    def sorted_neighbors(self):
        return sorted(self.neighbors)

    def __repr__(self):
        return f"({self.value})"

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

    def sorted_nodes(self):
        return dict(sorted(self.nodes.items()))

    def __repr__(self):
        nodes = self.sorted_nodes()
        graph_repr = ""
        for node_value, node_obj in nodes.items():
            neighbor_values = sorted([n.value for n in node_obj.neighbors])
            if neighbor_values:
                graph_repr += f"  {node_value} ->  {", ".join(neighbor_values)}\n"
        return graph_repr

def DeBruijn(Text, k):
    Debruijn_graph = Graph()
    for i in range(len(Text)-k+1):
        Debruijn_graph.add_edge(Text[i:i+k-1], Text[i+1:i+k])
    return Debruijn_graph

Text = "AAGATTCTCTAC"
k = 4
print(DeBruijn(Text, k))