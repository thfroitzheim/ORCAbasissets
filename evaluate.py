#!/bin/python3

import sys
import periodictable as pt

# create a dictionary of the elements
pesdict={"symb":[],"numb":[],"startline":[],"endline":[],"nbf":[],"npr":[]}
for el in pt.elements:
    if el.number == 0:
        continue
    pesdict["symb"].append(el.symbol)
    pesdict["numb"].append(el.number)
print(pesdict["symb"],pesdict["numb"])

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
k=0
for i in range(0,len(lines)):
    if "NewGTO" in lines[i].strip():
        pesdict["startline"].append(i+1)
    if "end" in lines[i].strip():
        pesdict["endline"].append(i)
        # print start and end line
        print(pesdict["startline"][k],pesdict["endline"][k])
        k=k+1

k=0
l=0
bf = []
exponents=[]
coefficients=[]
# go through all entries in the dictionary and read the basis functions
for i in range(1,len(pesdict["symb"])):
    exptmp=[]
    coefftmp=[]
    bfdict={"lnpr":[],"angmom":[]} # dictionary for the basis functions
    for j in range(pesdict["startline"][i],pesdict["endline"][i]):
        pesdict["nbf"].append(0)
        pesdict["npr"].append(0)
        if "S" in lines[j].strip():
            bfdict["angmom"].append("S")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            print(bfdict["angmom"][0],bfdict["lnpr"][0])
            pesdict["nbf"][i]=pesdict["nbf"][i]+1
            pesdict["npr"][i]=pesdict["npr"][i]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            print(coefftmp)
            l+=1
        if "P" in lines[j].strip():
            bfdict["angmom"].append("P")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            print(bfdict["angmom"][0],bfdict["lnpr"][0])
            pesdict["nbf"][k]=pesdict["nbf"][k]+1
            pesdict["npr"][k]=pesdict["npr"][k]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            print(coefftmp)
        if "D" in lines[j].strip():
            bfdict["angmom"].append("D")
            bfdict["lnpr"].append(int(lines[j].strip().split()[1]))
            print(bfdict["angmom"][0],bfdict["lnpr"][0])
            pesdict["nbf"][k]=pesdict["nbf"][k]+1
            pesdict["npr"][k]=pesdict["npr"][k]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(lines[m].strip().split()[1])
                coefftmp.append(lines[m].strip().split()[2])
            print(coefftmp)
        print(lines[j].strip())

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

    k=k+1