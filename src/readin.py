#!/bin/python3

# This script reads a Gaussian input file and extracts the basis set.
import periodictable as pt

def orcaformat(f):
    # create a dictionary of the elements
    pesdict={"symb":[],"numb":[],"startline":[],"endline":[],"nbf":[],"npr":[]}
    for el in pt.elements:
        if el.number == 0:
            continue
        elif el.number >= 87:
            break
        pesdict["symb"].append(el.symbol)
        pesdict["numb"].append(int(el.number))

    # read the file
    lines = f.readlines()
    for i in range(0,len(lines)):
        if "NewGTO" in lines[i].strip():
            pesdict["startline"].append(i+1)
        if "end" in lines[i].strip():
            pesdict["endline"].append(i)

    bf = []
    exponents=[]
    coefficients=[]
    # create a dictionary with element symbol, number, nbf, npr, list[angular momenta],
    #   list[exponents], list[coefficients]  
    basisset = {"symb":[],"numb":[],"nbf":[],"npr":[],"angmom":[],"lnpr":[],"exponents":[],"coefficients":[]}
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
            elif "P" in lines[j].strip():
                bfdict["angmom"].append("P")
            elif "D" in lines[j].strip():
                bfdict["angmom"].append("D")
            elif "F" in lines[j].strip():
                bfdict["angmom"].append("F")
            elif "G" in lines[j].strip():
                print("No support of F or higher functions.")
                exit()
            elif "end" in lines[j].strip():
                break
            else:
                continue
            num = int(lines[j].strip().split()[1])
            bfdict["lnpr"].append(num)
            pesdict["nbf"][i]=pesdict["nbf"][i]+1
            pesdict["npr"][i]=pesdict["npr"][i]+bfdict["lnpr"][l]
            for m in range(j+1,j+bfdict["lnpr"][l]+1):
                exptmp.append(float(lines[m].strip().split()[1]))
                coefftmp.append(float(lines[m].strip().split()[2]))
            l+=1

        # Development printouts
        # print(pesdict["symb"][i],pesdict["numb"][i],pesdict["nbf"][i],pesdict["npr"][i])
        #######################
        exponents.append(exptmp)
        coefficients.append(coefftmp)
        bf.append(bfdict)

        # Development printouts
        # print(bf[i])
        # print(exponents[i])
        # print(coefficients[i])
        #######################
        
        # fill the dictionary with the basis set information
        basisset["symb"].append(pesdict["symb"][i])
        basisset["numb"].append(pesdict["numb"][i])
        basisset["nbf"].append(pesdict["nbf"][i])
        basisset["npr"].append(pesdict["npr"][i])
        basisset["angmom"].append(bf[i]["angmom"])
        basisset["lnpr"].append(bf[i]["lnpr"])
        basisset["exponents"].append(exptmp)
        basisset["coefficients"].append(coefftmp)

        #end of iteration

    return basisset