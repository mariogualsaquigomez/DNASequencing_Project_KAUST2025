"""
String Spelled by a Genome Path Problem

Find the string spelled by a genome path.

Given: A sequence of k-mers Pattern1, ... , Patternn such that the last k - 1 symbols of Patterni are equal to the first k - 1 symbols of Patterni+1 for i from 1 to n-1.

Return: A string Text of length k+n-1 where the i-th k-mer in Text is equal to Patterni for all i.
"""
import glob


def prefix(text):
    return text[:-1]


def suffix(text):
    return text[1:]


def side_finder(pat_dict, pattern, direction):
    no_coincidences = True
    match direction:
        case 'begin':
            for pattern_comp in pat_dict:
                if (suffix(pattern_comp) == prefix(pattern)) & (pattern_comp != pattern):
                    no_coincidences = False
                    break
        case 'end':
            for pattern_comp in pat_dict:
                if (suffix(pattern) == prefix(pattern_comp)) & (pattern_comp != pattern):
                    no_coincidences = False
                    break
    return no_coincidences


#dict_pat_t = {'ACCGA': None, 'CCGAA': None, 'CGAAG': None, 'GAAGC': None, 'AAGCT': None}


#for p in dict_pat_t:
#    side_finder(dict_pat_t, p,'end')

def Reconstruction_seq(seqList):
    initial_seq = ""
    end_seq = ""
    seq_graph = {}
    for p in seqList:
        if side_finder(seqList, p, 'begin'):
            initial_seq = p
            continue
        if side_finder(seqList, p, 'end'):
            end_seq = p
            continue
        if (len(initial_seq) != 0 and len(end_seq) != 0):
            break
    seqList.pop(initial_seq)
    seqList.pop(end_seq)
    k = len(initial_seq)
    last_forward = initial_seq
    last_reverse = end_seq
    while seqList:
        for o in ['A', 'G', 'C', 'T']:
            if suffix(last_forward) + o in seqList:
                new_seq = suffix(last_forward) + o
                seq_graph[last_forward] = new_seq
                last_forward = new_seq
                seqList.pop(new_seq)
                break
            if o + prefix(last_reverse) in seqList:
                new_seq = o + prefix(last_reverse)
                seq_graph[new_seq] = last_reverse
                last_reverse = new_seq
                seqList.pop(new_seq)
                break
            continue
    seq_graph[last_forward] = last_reverse
    nodes_list = sorted([f"{key} -> {value}" for key, value in seq_graph.items()])
    return nodes_list

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
                print(content, end="", file=f)
            case int():
                print(str(content), end="", file=f)
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
    pattern_dict = dict()
    for l in file_load:
        pattern_dict[l.strip("\n")] = None
    seq_s = Reconstruction_seq(pattern_dict)
    write_file_txt(input_file, seq_s)
