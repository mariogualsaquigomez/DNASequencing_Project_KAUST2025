import glob


class Node:
    def __init__(self, value):
        self.value = value  # Unique identifier or data for the node
        self.neighbors = [] # List to store references to neighboring Node objects

    def add_neighbor(self, neighbor_node):
        #if neighbor_node not in self.neighbors: #For unique Nodes
            #self.neighbors.append(neighbor_node)
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
                graph_repr += f"{node_value} -> {",".join(neighbor_values)}\n"
        return graph_repr

def CompositeGraph(ListPatterns):
    Debruijn_graph = Graph()
    k = len(ListPatterns[0])
    for pattern in ListPatterns:
        Debruijn_graph.add_edge(pattern[:-1], pattern[1:])
    return Debruijn_graph

# Text = "AAGATTCTCTAC"
# k = 4
# print(DeBruijn(Text, k))

################### EVAL FUCTION ###########################
#Testing with files
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


# Getting txt files
folder_path = "./inputs"
input_files = glob.glob(f"{folder_path}/*.txt")

# #MODIFY THIS SECTION FOR EACH FUNCTION
for input_file in input_files:
    file_load = read_file_txt(input_file)
    ListKmer  = [l.strip() for l in file_load]
    graph = CompositeGraph(ListKmer)
    write_file_txt(input_file, graph.__repr__())
