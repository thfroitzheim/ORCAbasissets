#!/bin/python3

import sys

def take_second(elem):
    return elem[1]

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

autokcal=627.509
lines = f.readlines()

LCCSDT = {}

for i in range(0,len(lines)):
    if "CONF" in lines[i].strip():
        LCCSDT[lines[i].strip()] = float(lines[i+1].split()[3])

compound=sys.argv[1].split(".")[0]
LCCSDT=sorted(LCCSDT.items(), key=take_second)
DFT = {}
for CONF in LCCSDT:
    dft_file=compound+"/"+CONF[0]+"/ridft.out"
    try:
        f2=open(dft_file,"r")
    except:
        print("Could not find DFT calculation for conformer: "+CONF[0])
        sys.exit()
    lines=f2.readlines()
    DFT[CONF[0]]=float(lines[[i for i, s in enumerate(lines) if "total energy" in s][1]].split()[4])

lowest=LCCSDT[0]
for CONF in LCCSDT:
    #print(CONF[0]+" "+str((CONF[1]-lowest[1])*autokcal)+" "+str((DFT[CONF[0]]-DFT[lowest[0]])*autokcal))
    print(str((DFT[CONF[0]]-DFT[lowest[0]])*autokcal))
