"""
In “Find an Eulerian Cycle in a Graph”, we defined an Eulerian cycle. A path that traverses each edge of a graph exactly once (but does not necessarily return to its starting node is called an Eulerian path.
Eulerian Path Problem

Find an Eulerian path in a graph.

Given: A directed graph that contains an Eulerian path, where the graph is given in the form of an adjacency list.

Return: An Eulerian path in this graph.
"""
import glob

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
                
# Example usage
# graph = {
#     0: [2],
#     1: [3],
#     2: [1],
#     3: [0, 4],
#     6: [3, 7],
#     7: [8],
#     8: [9],
#     9: [6]
# }
# 
# path = eulerian_path(graph)
# if path:
#     print("Eulerian path:", " -> ".join(map(str, path)))
# else:
#     print("No Eulerian path exists")
# Getting txt files
if __name__ == "__main__":
    folder_path = "./inputs"
    input_files = glob.glob(f"{folder_path}/*.txt")

    # #MODIFY THIS SECTION FOR EACH FUNCTION
    for input_file in input_files:
        file_load = read_file_txt(input_file)
        file_load = [l.strip() for l in file_load]
        graph = {}
        for line in file_load:
            (node, neighbors) = line.split(" -> ")
            neighbors = neighbors.split(",")
            graph[node] = neighbors
        path = eulerian_path(graph)
        if path:
            solution = "->".join(map(str, path))
        else:
            solution = "The graph does not contain an Eulerian path"
        write_file_txt(input_file, solution)