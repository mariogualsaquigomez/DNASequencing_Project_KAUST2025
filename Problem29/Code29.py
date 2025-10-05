import glob
from collections import defaultdict


def eulerian_cycle(adj):
    # making a shallow copy
    g = {u: list(vs) for u, vs in adj.items()}

    # choose a start node with outgoing edges
    start = next((u for u in g if g[u]), None)

    #     print("start: ", start)
    stack, cycle = [start], []

    while stack:
        v = stack[-1]

        # if v exists, we pop from the adj_list, and append to stack
        if g[v]:
            w = g[v].pop()  # consume edge v->w
            stack.append(w)

        # if no vs under that g (all popped for that g), then we pop from stack and add to cycle
        else:
            popped = stack.pop()
            cycle.append(popped)

    #         print("\nstack: ", stack)
    #         print("cycle: ", cycle)
    #         print(g)

    # reverse to correct order
    cycle.reverse()

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


# Example graph
# graph = {
#         0: [3],
#         1: [0],
#         2: [1, 6],
#         3: [2],
#         4: [2],
#         5: [4],
#         6: [5, 8],
#         7: [9],
#         8: [7],
#         9: [6]
#     }
#
# if has_eulerian_cycle(graph):
#     cycle = eulerian_cycle(graph)
#     print("Eulerian cycle:", " -> ".join(map(str, cycle)))
# else:
#     print("The graph does not contain an Eulerian cycle")

# Example usage
if __name__ == "__main__":

    # Getting txt files
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
            graph[node] = graph.get(node, []) + neighbors
        if has_eulerian_cycle(graph):
            cycle = eulerian_cycle(graph)
            solution = "->".join(cycle)
        else:
            solution = "The graph does not contain an Eulerian cycle"
        write_file_txt(input_file, solution)