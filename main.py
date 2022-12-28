#!/bin/python3

import sys
from src.readin import orcaformat
from src.writebasis import orcabasissetcode

def print_help():
    print("Usage: python3 evaluate.py <input file>")
    print("Example: python3 evaluate.py input.gjf")
    print("This script reads a Gaussian input file and extracts the basis set.")
    print("The output is a dictionary with the following keys and values:")
    print("symb: list of the symbols of the elements")
    print("numb: list of the atomic numbers of the elements")
    print("startline: list of the line numbers where the basis functions start")
    print("endline: list of the line numbers where the basis functions end")
    print("nbf: list of the number of basis functions per element")
    print("npr: list of the number of primitives per element")
    print("lnpr: list of the number of primitives per basis function")
    print("angmom: list of the angular momentum of the basis functions")
    print("exponents: list of the exponents of the primitives")
    print("coefficients: list of the coefficients of the primitives")
    print("The dictionary is called pesdict.")
    print("The basis functions are stored in a list of dictionaries called bf.")
    print("The dictionary bf contains the keys lnpr and angmom.")
    print("The list of exponents and coefficients is called exponents and coefficients.")

# check if the input argument is given
try:
    str(sys.argv[1])
except:
    print("No input argument.")
    exit()
try:
    file = open(str(sys.argv[1]))
    print("File "+str(sys.argv[1])+" opened.")
except:
    print("Could not open file "+str(sys.argv[1])+".")
    exit()

try:
    str(sys.argv[2])
    if str(sys.argv[2]) == "-h":
        print_help()
        exit()
    elif str(sys.argv[2]) == "--help":
        print_help()
        exit()
    else:
        print("The last element is: "+str(sys.argv[2]))
        desiredelem = int(str(sys.argv[2]))
except:
    print("No second input argument.")
    desiredelem = 86

print(desiredelem)

# read the file
# basis is a dictionary with the following keys and values:
# symb: list of the symbols of the elements
# numb: list of the atomic numbers of the element
basis = orcaformat(file)

# print only the full basis function for the desired element
print("The number basis functions for the desired element is:")
print(basis["nbf"][desiredelem-1])
print("The number of primitives for the desired element is:")
print(basis["npr"][desiredelem-1])
print("The basis functions are:")
k=0
for i in range(0,basis["nbf"][desiredelem-1]):
    print("Basis function "+str(i+1)+":")
    print("  Angular momentum: "+basis["angmom"][desiredelem-1][i])
    print("  Number of primitives: "+str(basis["lnpr"][desiredelem-1][i]))
    print("  Exponents and coefficients:")
    for j in range(0,basis["lnpr"][desiredelem-1][i]):
        print(j+1)
        print("    "+str(basis["exponents"][desiredelem-1][k]))
        print("    "+str(basis["coefficients"][desiredelem-1][k]))
        k+=1


orcabasissetcode(basis)
