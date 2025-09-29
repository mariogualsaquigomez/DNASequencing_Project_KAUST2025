"""
Even after read breaking, most assemblies still have gaps in k-mer coverage, causing the de Bruijn graph to have missing edges, and so the search for an Eulerian path fails. In this case, biologists often settle on assembling contigs (long, contiguous segments of the genome) rather than entire chromosomes. For example, a typical bacterial sequencing project may result in about a hundred contigs, ranging in length from a few thousand to a few hundred thousand nucleotides. For most genomes, the order of these contigs along the genome remains unknown. Needless to say, biologists would prefer to have the entire genomic sequence, but the cost of ordering the contigs into a final assembly and closing the gaps using more expensive experimental methods is often prohibitive.

Fortunately, we can derive contigs from the de Bruijn graph. A path in a graph is called non-branching if in(v) = out(v) = 1 for each intermediate node v of this path, i.e., for each node except possibly the starting and ending node of a path. A maximal non-branching path is a non-branching path that cannot be extended into a longer non-branching path. We are interested in these paths because the strings of nucleotides that they spell out must be present in any assembly with a given k-mer composition. For this reason, contigs correspond to strings spelled by maximal non-branching paths in the de Bruijn graph.
Contig Generation Problem

Generate the contigs from a collection of reads (with imperfect coverage).

Given: A collection of k-mers Patterns.

Return: All contigs in DeBruijn(Patterns). (You may return the strings in any order.)
"""

from collections import defaultdict


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

def find_contigs(graph):
    """
    Find all contigs (maximal non-branching paths) in a de Bruijn graph.
    
    Args:
        graph: A Graph object representing the de Bruijn graph
        
    Returns:
        list: A list of paths, where each path is a list of node values representing a contig
    """
    # Helper function to count incoming edges to a node
    def count_in_edges(node_value):
        count = 0
        for node in graph.nodes.values():
            for neighbor in node.neighbors:
                if neighbor.value == node_value:
                    count += 1
        return count

    # Helper function to check if a node has exactly one incoming and one outgoing edge
    def is_1_in_1_out(node_value):
        in_degree = count_in_edges(node_value)
        out_degree = len(graph.nodes[node_value].neighbors)
        return in_degree == 1 and out_degree == 1

    # def find_non_branching_path(start_node):
    #     """Find a maximal non-branching path starting from given node"""
    #     path = [start_node.value]
    #     current = start_node
    #
    #     while current.neighbors:
    #         # Get the next node
    #         next_node = current.neighbors[0]
    #
    #         # If next node is not 1-in-1-out, stop
    #         if not is_1_in_1_out(next_node.value):
    #             path.append(next_node.value)
    #             break
    #
    #         path.append(next_node.value)
    #         current = next_node
    #
    #         # If we've reached a node that's already been visited, stop
    #         if next_node.value == start_node.value:
    #             break
    #
    #     return path

    contigs = []
    visited = set()

    # Find all nodes that are not 1-in-1-out or have no outgoing edges
    for node_value, node in graph.nodes.items():
        if not is_1_in_1_out(node_value) and node.neighbors:
            # Start a new non-branching path from each outgoing edge
            for neighbor in node.neighbors:
                path = [node_value, neighbor.value]
                current = neighbor

                # Extend the path while possible
                while is_1_in_1_out(current.value) and current.neighbors:
                    next_node = current.neighbors[0]
                    path.append(next_node.value)
                    current = next_node

                contigs.append(path)

    # Find isolated cycles (all nodes are 1-in-1-out)
    # for node_value, node in graph.nodes.items():
    #     if is_1_in_1_out(node_value) and node_value not in visited:
    #         path = find_non_branching_path(node)
    #         if len(path) > 1:
    #             contigs.append(path)
    #             visited.update(path)
    
    return contigs


# Example usage:
if __name__ == "__main__":
    # Create a sample de Bruijn graph
    kmers = ['ATG','ATG','TGT','TGG','CAT','GGA','GAT','AGA']
    k = 3
    graph = CompositeGraph(kmers, k)

    # Find contigs
    contigs = find_contigs(graph)

    # Print results
    print("Contigs found:")
    for contig in contigs:
        # Reconstruct the sequence from the path
        sequence = contig[0] + ''.join(node[-1] for node in contig[1:])
        print(sequence)