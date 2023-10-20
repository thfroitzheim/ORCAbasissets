import os

# dictionary for relationship between angular momenta
# in letters ("S","P","D","F") and numbers (0,1,2,3)
angmomdict = {"S": 0, "P": 1, "D": 2, "F": 3, "G": 4, "H": 5, "I": 6}


def orcabasissetcode(bas):
    # Write the basis set in the format of the ORCA input file
    # The input is a dictionary with the following keys and values:
    path = "output"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Output directory was created!")

    ofile = open("output/basis_orcasource.txt", "w")
    for i in range(0, len(bas["symb"])):
        l = 0
        ofile.write("  // --------------------------------------------------------\n")
        ofile.write(
            "  // element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")\n"
        )
        ofile.write("  // --------------------------------------------------------\n")
        ofile.write(
            "  B.Init({0:4d},{1:4d});\n".format(
                int(bas["numb"][i]), int((bas["nbf"][i]))
            )
        )
        for j in range(0, bas["nbf"][i]):
            ofile.write("  // Basis function " + bas["angmom"][i][j] + "\n")
            ofile.write(
                "  BG[{0:3d}][{1:3d}].l     ={2:2d};\n".format(
                    bas["numb"][i], j, angmomdict[bas["angmom"][i][j]]
                )
            )
            ofile.write(
                "  BG[{0:3d}][{1:3d}].ng    ={2:2d};\n".format(
                    bas["numb"][i], j, bas["lnpr"][i][j]
                )
            )
            for k in range(0, bas["lnpr"][i][j]):
                ofile.write(
                    "  BG[{0:3d}][{1:3d}].a[{2:2d}] ={3:25.10f};   BG[{0:3d}][{1:3d}].d[{2:2d}] ={4:25.10f};\n".format(
                        bas["numb"][i],
                        j,
                        k,
                        bas["exponents"][i][l],
                        bas["coefficients"][i][l],
                    )
                )
                l += 1
        ofile.write("\n\n")
    ofile.close()


def orcaecpcode(ecp):
    # Write the ECP in the format of the ORCA input file
    # The input is a dictionary with the following keys and values:
    path = "output"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Output directory was created!")

    ofile = open("output/ecp_orcasource.txt", "w")
    for i in range(0, len(ecp["symb"])):
        l = 0
        ofile.write("  // --------------------------------------------------------\n")
        ofile.write(
            "  // element no " + str(ecp["numb"][i]) + " (" + ecp["symb"][i] + ")\n"
        )
        ofile.write("  // --------------------------------------------------------\n")
        ofile.write(
            "  E->U[ {0:3d} ] = new ecpPotential;\n".format(int(ecp["numb"][i]))
        )
        ofile.write(
            "  E->U[ {0:3d} ]->initialize({1:4d},{2:4d},{3:4d} );\n".format(
                ecp["numb"][i],
                int(angmomdict[ecp["lmax"][i].upper()]),
                ecp["ncore"][i],
                ecp["nbf"][i],
            )
        )
        ofile.write("  E->U[ {0:3d} ]->element    ={0:4d};\n".format(ecp["numb"][i]))
        ofile.write(
            "  CopyECPCommentary( E->U[ {0:3d} ], \
all_ecpname, all_comment, all_citation, all_source );\n".format(
                ecp["numb"][i]
            )
        )
        ofile.write("  E->U[ {0:3d} ]->cpp        = NULL;\n".format(ecp["numb"][i]))
        ofile.write("  EG = E->U[ {0:3d} ]->U_l;\n\n".format(ecp["numb"][i]))
        for j in range(0, ecp["nbf"][i]):
            ofile.write("  EG[{0:4d} ].l ={0:2d};\n".format(j))
            ofile.write("  EG[{0:4d} ].K ={1:2d};\n".format(j, ecp["lnpr"][i][j]))
            for k in range(0, ecp["lnpr"][i][j]):
                ofile.write(
                    "  EG[{0:4d} ].p[{1:4d} ].a ={2:23.12f} ;".format(
                        j, k, ecp["exponents"][i][l]
                    )
                )
                ofile.write(
                    "  EG[{0:4d} ].p[{1:4d}  ].d ={2:23.12f} ;".format(
                        j, k, ecp["coefficients"][i][l]
                    )
                )
                ofile.write(
                    "  EG[{0:4d} ].p[{1:4d}  ].n ={2:4.1f} ;\n".format(
                        j, k, float(ecp["ecpnfactor"][i][l])
                    )
                )
                l += 1
        ofile.write("\n\n")
