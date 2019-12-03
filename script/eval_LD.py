#!/usr/bin/env python3
# Evaluate tokenisation result based on Levenshtein distance with the following edit costs
# insertion: 1
# deletion: 1
# substitution: 1
# no cost for substitution of a letter for itself

import re
import sys
import difflib
import numpy as np

# Split string into list of characters
def split(string):
    return [char for char in string]

# Return Levenshtein distance
def LD(source, target):
    insertion = 1
    deletion = 1
    substitution = 1
    len_source = len(source)
    len_target = len(target)
    dist_matrix = np.zeros((len_source+1,len_target+1))
    for i in range(len_source):
        dist_matrix[i+1,0] = dist_matrix[i,0] + insertion
    for i in range(len_target):
        dist_matrix[0,i+1] = dist_matrix[0,i] + insertion
    for i in range(len_source):
        for j in range(len_target):
            # Substitution cost is zero for the same character
            if(source[i]==target[j]):
                dist_matrix[i+1,j+1] = min(dist_matrix[i+1,j]+insertion,
                                           dist_matrix[i,j+1]+deletion,
                                           dist_matrix[i,j])
            # General case
            else:
                dist_matrix[i+1,j+1] = min(dist_matrix[i+1,j]+insertion,
                                           dist_matrix[i,j+1]+deletion,
                                           dist_matrix[i,j]+substitution)
    return dist_matrix[len_source,len_target]

def main():
    # Read my tokenisation results from cat command
    my_data = sys.stdin.read()

    # Read gold result from file
    with open("file.tok.gold") as file:
        gold_data = file.read()

    # Find sentences with differences
    diff = difflib.unified_diff(my_data.splitlines(), gold_data.splitlines())
    diff_list = list(diff)
    diff_my = [sentence[1:] for sentence in diff_list if sentence.startswith("-")]
    diff_gold = [sentence[1:] for sentence in diff_list if sentence.startswith("+")]
    diff_tuple = list(zip(diff_my, diff_gold))
    diff_tuple = diff_tuple[1:] # remove leading plus and minus sign from difflib
    
    # Find total LD for all differences
    LD_total = 0
    for pair in diff_tuple:
        LD_total += LD(pair[0],pair[1])
    with open("file.tok.score","w+") as output:
        output.write(str(LD_total))

if __name__== "__main__":
  main()