"""
This module contains functions to write the basis set in the format of
different quantum chemistry programs.
"""

import os
import numpy as np

# dictionary for relationship between angular momenta
# in letters ("S","P","D","F") and numbers (0,1,2,3)
angmomdict = {"S": 0, "P": 1, "D": 2, "F": 3, "G": 4, "H": 5, "I": 6}


def orcabasissetcode(bas):
    """
    Write the basis set in the format of the ORCA input file
    """
    # Write the basis set in the format of the ORCA input file
    # The input is a dictionary with the following keys and values:
    path = "output"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Output directory was created!")

    ofile = open("output/basis_orcasource.txt", "w", encoding="utf-8")
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
                    "  BG[{0:3d}][{1:3d}].a[{2:2d}] ={3:25.10f};   \
BG[{0:3d}][{1:3d}].d[{2:2d}] ={4:25.10f};\n".format(
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
    """
    Write the ECP in the format of the ORCA input file
    """
    # Write the ECP in the format of the ORCA input file
    # The input is a dictionary with the following keys and values:
    path = "output"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Output directory was created!")

    ofile = open("output/ecp_orcasource.txt", "w", encoding="utf-8")
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


def xtb_tblite_format_basis(bas):
    """
    Write the basis set in the format of the xtb tblite file
    """
    path = "output"
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("Output directory was created!")

    # find out the maximal number of primitive functions per basis function
    # in the whole basis set
    maxnpr = 0
    for i in range(0, len(bas["nbf"])):
        for j in range(0, bas["nbf"][i]):
            if bas["lnpr"][i][j] > maxnpr:
                maxnpr = bas["lnpr"][i][j]
    print("Maximum number of primitive functions per basis function: " + str(maxnpr))
    maxshell = 7

    # open("output/basis_xtbsource.txt", "w", encoding="utf-8")
    with open("output/basis_xtbsource.txt", "w", encoding="utf-8") as ofile:
        # iterate over all elements until Z=86
        print("----------- EXPONENTS -----------")
        for i in range(0, len(bas["symb"])):
            if bas["numb"][i] > 57 and bas["numb"][i] < 72:
                continue
            print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
            # write the basis set in Fortran format as follows:
            # create one Fortran array with the exponents
            # and one with the coefficients for each element
            # the arrays should have max(nprim) x max(nbf) elements
            # and are setup with zeros for the unused elements
            # and using the Fortran "reshape" function to create the
            # correct dimensions
            exponents = np.zeros((maxnpr, maxshell), dtype=float)
            # go through all exponents of the basis functions of the element i
            m = 0
            for j in range(0, bas["nbf"][i]):
                for k in range(0, bas["lnpr"][i][j]):
                    exponents[k][j] = bas["exponents"][i][m]
                    m += 1

            # print the numpy array in nice format to screen
            print(exponents)

            # write the exponents in Fortran format
            print(f"exponents(:, :, {i+1:2d}) = reshape([&", file=ofile)
            print(exponents.shape[0], exponents.shape[1])
            for j in range(exponents.shape[1]):
                print("& ", file=ofile, end="")
                for k in range(exponents.shape[0] - 1):
                    print(f"{exponents[k][j]:15.10f}_wp, ", file=ofile, end="")
                if j == exponents.shape[1] - 1:
                    print(
                        f"{exponents[-1][j]:15.10f}_wp], (/max_prim, max_shell/))",
                        file=ofile,
                    )
                else:
                    print(f"{exponents[-1][j]:15.10f}_wp, &", file=ofile)
            print("", file=ofile)

        print("----------- COEFFICIENTS -----------")
        for i in range(0, len(bas["symb"])):
            if bas["numb"][i] > 57 and bas["numb"][i] < 72:
                continue
            print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
            coefficients = np.zeros((maxnpr, maxshell), dtype=float)
            # go through all coefficients of the basis functions of the element i
            m = 0
            for j in range(0, bas["nbf"][i]):
                print("Basis function " + str(j) + ":")
                for k in range(0, bas["lnpr"][i][j]):
                    coefficients[k][j] = bas["coefficients"][i][m]
                    m += 1

            # print the numpy array in nice format to screen
            print(coefficients)

            # write the coefficients in Fortran format
            print(f"coefficients(:, :, {i+1:2d}) = reshape([&", file=ofile)
            for j in range(coefficients.shape[1]):
                print("& ", file=ofile, end="")
                for k in range(coefficients.shape[0] - 1):
                    print(f"{coefficients[k][j]:15.10f}_wp, ", file=ofile, end="")
                if j == coefficients.shape[1] - 1:
                    print(
                        f"{coefficients[-1][j]:15.10f}_wp], (/max_prim, max_shell/))",
                        file=ofile,
                    )
                else:
                    print(f"{coefficients[-1][j]:15.10f}_wp, &", file=ofile)
            print("", file=ofile)

        if("coeff_env" in bas):
            print("----------- COEFFICIENTS ENVIRONMENT-DEPENDENCE-----------")
            for i in range(0, len(bas["symb"])):
                if bas["numb"][i] > 57 and bas["numb"][i] < 72:
                    continue
                print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
                coefficients_env = np.zeros((maxnpr, maxshell), dtype=float)
                # go through all coefficients of the basis functions of the element i
                m = 0
                for j in range(0, bas["nbf"][i]):
                    print("Basis function " + str(j) + ":")
                    for k in range(0, bas["lnpr"][i][j]):
                        coefficients_env[k][j] = bas["coeff_env"][i][m]
                        m += 1

                # print the numpy array in nice format to screen
                print(coefficients_env)

                # write the coefficients in Fortran format
                print(f"coefficients_env(:, :, {i+1:2d}) = reshape([&", file=ofile)
                for j in range(coefficients_env.shape[1]):
                    print("& ", file=ofile, end="")
                    for k in range(coefficients_env.shape[0] - 1):
                        print(f"{coefficients_env[k][j]:15.10f}_wp, ", file=ofile, end="")
                    if j == coefficients_env.shape[1] - 1:
                        print(
                            f"{coefficients_env[-1][j]:15.10f}_wp], (/max_prim, max_shell/))",
                            file=ofile,
                        )
                    else:
                        print(f"{coefficients_env[-1][j]:15.10f}_wp, &", file=ofile)
                print("", file=ofile)

        if("env_k1" in bas):
            print("----------- CHARGE-DEPENDENCE PARAMETER K1 -----------", file=ofile)
            print(f"\nreal(wp), parameter :: p_k1(86) = ([&", file=ofile)
            l=0
            for i in range(0, len(bas["symb"])):
                print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
                print("The charge-dependence parameter k1 for the desired element is:")
                print(bas["env_k1"][i])
                tmpk1 = bas["env_k1"][i]
                l += 1
                if l >= 8:
                    print(f"{tmpk1:15.10f}_wp, &", file=ofile)
                    l = 0
                    continue
                elif i >= len(bas["symb"]) - 1:
                    print(f"{tmpk1:15.10f}_wp]", file=ofile)
                elif l <= 1:
                    print(f"& {tmpk1:15.10f}_wp, ", file=ofile, end="")
                else:
                    print(f"{tmpk1:15.10f}_wp, ", file=ofile, end="")

        if("env_k2" in bas):
            print("----------- CN-DEPENDENCE PARAMETER K2 -----------", file=ofile)
            print(f"\nreal(wp), parameter :: p_k2(86) = ([&", file=ofile)
            l=0
            for i in range(0, len(bas["symb"])):
                print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
                print("The CN-dependence parameter k2 for the desired element is:")
                print(bas["env_k2"][i])
                tmpk1 = bas["env_k2"][i]
                l += 1
                if l >= 8:
                    print(f"{tmpk1:15.10f}_wp, &", file=ofile)
                    l = 0
                    continue
                elif i >= len(bas["symb"]) - 1:
                    print(f"{tmpk1:15.10f}_wp]", file=ofile)
                elif l <= 1:
                    print(f"& {tmpk1:15.10f}_wp, ", file=ofile, end="")
                else:
                    print(f"{tmpk1:15.10f}_wp, ", file=ofile, end="")

        if("env_k3" in bas):
            print("----------- MIXED-DEPENDENCE PARAMETER K3 -----------", file=ofile)
            print(f"\nreal(wp), parameter :: p_k3(86) = ([&", file=ofile)
            l=0
            for i in range(0, len(bas["symb"])):
                print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
                print("The CN-dependence parameter k3 for the desired element is:")
                print(bas["env_k3"][i])
                tmpk1 = bas["env_k3"][i]
                l += 1
                if l >= 8:
                    print(f"{tmpk1:15.10f}_wp, &", file=ofile)
                    l = 0
                    continue
                elif i >= len(bas["symb"]) - 1:
                    print(f"{tmpk1:15.10f}_wp]", file=ofile)
                elif l <= 1:
                    print(f"& {tmpk1:15.10f}_wp, ", file=ofile, end="")
                else:
                    print(f"{tmpk1:15.10f}_wp, ", file=ofile, end="")

        # print the number of basis functions and primitives for each element
        print("----------- NUMBER OF BASIS FUNCTIONS -----------", file=ofile)
        print("\ninteger, parameter :: nshell(max_elem) = [ &", file=ofile)
        l = 0
        for i in range(0, len(bas["symb"])):
            print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
            print("The number basis functions for the desired element is:")
            print(bas["nbf"][i])
            if bas["nbf"][i] > 7:
                tmpbasnbf = 0
            else:
                tmpbasnbf = bas["nbf"][i]
            l += 1
            if l >= 20:
                print(f"{tmpbasnbf}, &", file=ofile)
                l = 0
                continue
            elif i >= len(bas["symb"]) - 1:
                print(f"{tmpbasnbf}]", file=ofile)
            elif l <= 1:
                print(f"& {tmpbasnbf}, ", file=ofile, end="")
            else:
                print(f"{tmpbasnbf}, ", file=ofile, end="")

        # print the number of primitives for each basis function of each element
        print("----------- NUMBER OF PRIMITIVES -----------", file=ofile)
        print(
            "\ninteger, parameter :: n_prim(highest_elem, max_shell) = reshape([&",
            file=ofile,
        )
        l = 0
        for i in range(0, len(bas["symb"])):
            print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
            print("The number of primitives for the desired element is:")
            print(bas["npr"][i])
            for j in range(0, maxshell):
                if bas["nbf"][i] > 7:
                    tmpbasnpr = 0
                else:
                    if j >= bas["nbf"][i]:
                        tmpbasnpr = 0
                    else:
                        tmpbasnpr = bas["lnpr"][i][j]
                l += 1
                if l >= 21:
                    print(f"{tmpbasnpr}, & ! up to element: {i+1}", file=ofile)
                    l = 0
                elif i >= len(bas["symb"]) - 1 and j >= maxshell - 1:
                    print(f"{tmpbasnpr}]", file=ofile)
                elif l <= 1:
                    print(f"& {tmpbasnpr}, ", file=ofile, end="")
                else:
                    print(f"{tmpbasnpr}, ", file=ofile, end="")

        # print the angular momentum for each basis function of each element
        print("----------- ANGULAR MOMENTUM -----------", file=ofile)
        print(
            "\ninteger, parameter :: angmom(max_elem, max_shell) = reshape([&",
            file=ofile,
        )
        l = 0
        for i in range(0, len(bas["symb"])):
            print("Element no " + str(bas["numb"][i]) + " (" + bas["symb"][i] + ")")
            print("The angular momentum for the desired element is:")
            print(bas["angmom"][i])
            for j in range(0, maxshell):
                if bas["nbf"][i] > 7:
                    tmpbasangmom = 0
                else:
                    if j >= bas["nbf"][i]:
                        tmpbasangmom = 0
                    else:
                        tmpbasangmom = angmomdict[bas["angmom"][i][j]]
                l += 1
                if l >= 21:
                    print(f"{tmpbasangmom}, & ! up to element: {i+1}", file=ofile)
                    l = 0
                elif i >= len(bas["symb"]) - 1 and j >= maxshell - 1:
                    print(f"{tmpbasangmom}]", file=ofile)
                elif l <= 1:
                    print(f"& {tmpbasangmom}, ", file=ofile, end="")
                else:
                    print(f"{tmpbasangmom}, ", file=ofile, end="")
