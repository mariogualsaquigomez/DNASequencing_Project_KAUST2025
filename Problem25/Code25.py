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
    initial_seq = ''
    end_seq = ''
    reconstructed_seq = ''
    d = len(seqList)
    for p in seqList:
        if side_finder(seqList, p, 'begin'):
            initial_seq = p
            continue
        if side_finder(seqList, p, 'end'):
            end_seq = p
            continue
        if (initial_seq != '' and end_seq != ''):
            break
    seqList.pop(initial_seq)
    seqList.pop(end_seq)
    k = len(initial_seq)
    while seqList:
        for o in ['A', 'G', 'C', 'T']:
            if suffix(initial_seq[-k:])+ o in seqList:
                initial_seq = initial_seq + o
                seqList.pop(initial_seq[-k:])
                break
            if o + prefix(end_seq[:k]) in seqList:
                end_seq = o  + end_seq
                seqList.pop(end_seq[:k])
                break
    if suffix(initial_seq[-k:]) == prefix(end_seq[:k]):
        reconstructed_seq = initial_seq + end_seq[k - 1:]
    return reconstructed_seq


#Reconstruction(dict_pat_t)

# RECURRENT FUNCTION
# def Reconstruction_seq(pattern_dict, last_key = None):
#     if len(pattern_dict) == 1:
#         if last_key is None:
#             return next(iter(pattern_dict))
#         return ""
#     if last_key == None:
#         firstpattern = next(iter(pattern_dict))
#         return firstpattern + Reconstruction_seq(pattern_dict, firstpattern)
#     pattern_dict.pop(last_key)
#     for key in pattern_dict:
#         #print(prefix(last_key)," == ",suffix(key))
#         if suffix(last_key) == prefix(key):
#             return key[-1] + Reconstruction_seq(pattern_dict, key)

#############################################################################################
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
