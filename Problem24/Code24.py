"""
Given a string Text, its k-mer composition Compositionk(Text) is the collection of all k-mer substrings of Text (including repeated k-mers). For example,

Composition3(TATGGGGTGC) = {ATG, GGG, GGG, GGT, GTG, TAT, TGC, TGG}

Note that we have listed k-mers in lexicographic order (i.e., how they would appear in a dictionary) rather than in the order of their appearance in TATGGGGTGC. We have done this because the correct ordering of the reads is unknown when they are generated.
String Composition Problem

Generate the k-mer composition of a string.

Given: An integer k and a string Text.

Return: Compositionk(Text) (the k-mers can be provided in any order).
"""
import glob
import sys


def Composition(k, text): #Composition function, gets all kmers in lexicographic order
    composition_list = {} # dictionary to save kmers
    for i in range(len(text)-k+1): # loop to explore all k-pattern windows and adding in dictionary
        composition_list[text[i:i+k]] = None #Update kmer key with None Value, the only keys are working
    return sorted(composition_list) #gives the ordered output with all kmers in the Sequence


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


if __name__ == "__main__":
    # Getting txt files
    folder_path = "./inputs"
    input_files = glob.glob(f"{folder_path}/*.txt")

    #MODIFY THIS SECTION FOR EACH FUNCTION
    for input_file in input_files:
        file_load = read_file_txt(input_file)
        composition_s = Composition(int(file_load[0].strip()), file_load[1].strip())
        write_file_txt(input_file, composition_s)

