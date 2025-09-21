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

def Reconstruction_seq(pattern_dict, last_key = None):
    if len(pattern_dict) == 1:
        if last_key is None:
            return next(iter(pattern_dict))
        return ""
    if last_key == None:
        firstpattern = next(iter(pattern_dict))
        return firstpattern + Reconstruction_seq(pattern_dict, firstpattern)
    pattern_dict.pop(last_key)
    for key in pattern_dict:
        #print(prefix(last_key)," == ",suffix(key))
        if suffix(last_key) == prefix(key):
            return key[-1] + Reconstruction_seq(pattern_dict, key)

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
                print(content, end="", file= f)
            case int():
                print(str(content), end="", file= f)
            case list():
                for text in content:
                    print(str(text), end="\n", file= f)
            case set():
                for text in content:
                    print(str(text), end="\n", file=f)
            case dict():
                for key in content:
                    print(str(key), end="\n", file= f)

# Getting txt files
folder_path = "./inputs"
input_files = glob.glob(f"{folder_path}/*.txt")

#MODIFY THIS SECTION FOR EACH FUNCTION
for input_file in input_files:
    file_load = read_file_txt(input_file)
    pattern_dict = dict()
    for l in file_load:
        pattern_dict[l.strip("\n")] = None
    seq_s = Reconstruction_seq(pattern_dict)
    write_file_txt(input_file, seq_s)