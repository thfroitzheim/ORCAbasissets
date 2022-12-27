#!/bin/python3

import sys
import periodictable as pt

# create a dictionary of the elements
pesdict={"symb":[],"numb":[],"startline":[],"endline":[],"nbf":[],"npr":[]}
for el in pt.elements:
    if el.number == 0:
        continue
    elif el.number >= 87:
        break
    pesdict["symb"].append(el.symbol)
    pesdict["numb"].append(el.number)

# check if the input argument is given
try:
    str(sys.argv[1])
except:
    print("No input argument.")
    exit()
try:
    f = open(str(sys.argv[1]))
except:
    print("Could not open file "+str(sys.argv[1])+".")
    exit()

# read the file
lines = f.readlines()
for i in range(0,len(lines)):
    if "NewGTO" in lines[i].strip():
        pesdict["startline"].append(i+1)
    if "end" in lines[i].strip():
        pesdict["endline"].append(i)

k=0
bf = []
exponents=[]
coefficients=[]
# go through all entries in the dictionary and read the basis functions
for i in range(0,len(pesdict["symb"])):
    l=0
    exptmp=[]
    coefftmp=[]
    bfdict={"lnpr":[],"angmom":[]} # dictionary for the basis functions
    # set number of basis functions and primitives to zero for each element
    pesdict["nbf"].append(0)
    pesdict["npr"].append(0)
    for j in range(pesdict["startline"][i],pesdict["endline"][i]):
        if "S" in lines[j].strip():
            bfdict["angmom"].append("S")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            # increase number of basis functions "nbf" by 1 and number of primitives "npr" by the number of primitives in the current basis function
            pesdict["nbf"][i]=pesdict["nbf"][i]+1
            pesdict["npr"][i]=pesdict["npr"][i]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            l+=1
        if "P" in lines[j].strip():
            bfdict["angmom"].append("P")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            pesdict["nbf"][i]=pesdict["nbf"][i]+1
            pesdict["npr"][i]=pesdict["npr"][i]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            l+=1
        if "D" in lines[j].strip():
            bfdict["angmom"].append("D")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            pesdict["nbf"][i]=pesdict["nbf"][i]+1
            pesdict["npr"][i]=pesdict["npr"][i]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            l+=1

    # Development printouts
    print(pesdict["symb"][i],pesdict["numb"][i],pesdict["nbf"][i],pesdict["npr"][i])
    #######################
    exponents.append(exptmp)
    coefficients.append(coefftmp)
    bf.append(bfdict)

    # Development printouts
    print(bf[k])
    print(exponents[k])
    print(coefficients[k])
    #######################

    k+=1