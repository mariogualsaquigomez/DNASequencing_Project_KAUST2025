"""
Even after read breaking, most assemblies still have gaps in k-mer coverage, causing the de Bruijn graph to have missing edges, and so the search for an Eulerian path fails. In this case, biologists often settle on assembling contigs (long, contiguous segments of the genome) rather than entire chromosomes. For example, a typical bacterial sequencing project may result in about a hundred contigs, ranging in length from a few thousand to a few hundred thousand nucleotides. For most genomes, the order of these contigs along the genome remains unknown. Needless to say, biologists would prefer to have the entire genomic sequence, but the cost of ordering the contigs into a final assembly and closing the gaps using more expensive experimental methods is often prohibitive.

Fortunately, we can derive contigs from the de Bruijn graph. A path in a graph is called non-branching if in(v) = out(v) = 1 for each intermediate node v of this path, i.e., for each node except possibly the starting and ending node of a path. A maximal non-branching path is a non-branching path that cannot be extended into a longer non-branching path. We are interested in these paths because the strings of nucleotides that they spell out must be present in any assembly with a given k-mer composition. For this reason, contigs correspond to strings spelled by maximal non-branching paths in the de Bruijn graph.
Contig Generation Problem

Generate the contigs from a collection of reads (with imperfect coverage).

Given: A collection of k-mers Patterns.

Return: All contigs in DeBruijn(Patterns). (You may return the strings in any order.)
"""

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


def MaximalNonBranchingPaths(graph):
    # Calculate in-degrees and out-degrees
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for node_val, node_obj in graph.nodes.items():
        out_degree[node_val] = len(node_obj.neighbors)
        for neighbor in node_obj.neighbors:
            in_degree[neighbor.value] += 1

    paths = []
    nodes_in_paths = set()

    # Find paths starting from non-1-in-1-out nodes
    for v_value in graph.nodes:
        is_1_in_1_out = in_degree[v_value] == 1 and out_degree[v_value] == 1
        if not is_1_in_1_out:
            if out_degree[v_value] > 0:
                for w_node in graph.nodes[v_value].neighbors:
                    path = [v_value, w_node.value]
                    nodes_in_paths.add(v_value)
                    nodes_in_paths.add(w_node.value)

                    current_node = w_node.value
                    while in_degree[current_node] == 1 and out_degree[current_node] == 1:
                        next_node = graph.nodes[current_node].neighbors[0]
                        path.append(next_node.value)
                        nodes_in_paths.add(next_node.value)
                        current_node = next_node.value

                    paths.append(path)

    # Find isolated cycles from the remaining nodes
    all_nodes = set(graph.nodes.keys())
    remaining_nodes = all_nodes - nodes_in_paths

    while remaining_nodes:
        start_node = remaining_nodes.pop()

        cycle_path = [start_node]
        current_node = start_node

        # Traverse the cycle
        next_node = graph.nodes[current_node].neighbors[0]
        while next_node.value != start_node:
            cycle_path.append(next_node.value)
            if next_node.value in remaining_nodes:
                remaining_nodes.remove(next_node.value)
            next_node = graph.nodes[next_node.value].neighbors[0]

        cycle_path.append(start_node)
        paths.append(cycle_path)

    return paths

################### EVAL FUCTION ###########################
# Testing with files
def read_file_txt(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.readlines()
            return content
    except FileNotFoundError:
        print(f"Error File not found at {file_path}")
    except Exception as error:
        print(f"Error while reading file {file_path}: {error}")


def write_file_txt(file_path, content):
    name_split = file_path.split("/")
    output_name = f"./outputs/{name_split[-1].strip(".txt")}_output.txt"
    with open(output_name, "w") as f:
        match content:
            case str():
                print(content, file=f)
            case int():
                print(str(content), file=f)
            case list():
                for text in content:
                    print(str(text), end="\n", file=f)
            case set():
                for text in content:
                    print(str(text), end="\n", file=f)
            case dict():
                for key in content:
                    print(str(key), end="\n", file=f)


if __name__ == "__main__":
    # Getting Files
    folder_path = "./inputs"
    input_files = glob.glob(f"{folder_path}/*.txt")

    # #MODIFY THIS SECTION FOR EACH FUNCTION
    for input_file in input_files:
        file_load = read_file_txt(input_file)
        file_load = [l.strip() for l in file_load]
        graph = Graph()
        for line in file_load:
            node, neigbours = line.split("->")
            node = node.strip()
            neigbours = neigbours.split(',')
            for neighbor in neigbours:
                neighbor = neighbor.strip()
                graph.add_edge(node, neighbor)
        # Find contigs
        branches = MaximalNonBranchingPaths(graph)
        # Print results
        sequences = []
        for b in branches:
            # Reconstruct the sequence from the path
            sequences.append('->'.join(node for node in b))
        solution = "\n".join(sequences)
        write_file_txt(input_file, solution)