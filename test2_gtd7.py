"""
12/19/2013
Author: Joshua Milas
Python Version: 3.3.2

The NRLMSISE-00 model 2001 ported to python
Based off of Dominik Brodowski 20100516 version available here
http://www.brodo.de/english/pub/nrlmsise/

This is the test program, and the output should be compaired to
/* -------------------------------------------------------------------- */
/* ---------  N R L M S I S E - 0 0    M O D E L    2 0 0 1  ---------- */
/* -------------------------------------------------------------------- */

/* This file is part of the NRLMSISE-00  C source code package - release
 * 20041227
 *
 * The NRLMSISE-00 model was developed by Mike Picone, Alan Hedin, and
 * Doug Drob. They also wrote a NRLMSISE-00 distribution package in
 * FORTRAN which is available at
 * http://uap-www.nrl.navy.mil/models_web/msis/msis_home.htm
 *
 * Dominik Brodowski implemented and maintains this C version. You can
 * reach him at mail@brodo.de. See the file "DOCUMENTATION" for details,
 * and check http://www.brodo.de/english/pub/nrlmsise/index.html for
 * updated releases of this package.
 */
"""

import time
from nrlmsise_00_header import *
from nrlmsise_00 import *

def test2_gtd7():
    output = nrlmsise_output()
    Input = nrlmsise_input()
    flags = nrlmsise_flags()
    aph = ap_array()

    for i in range(7):
        aph.a[i]=100
    flags.switches[0] = 0
    for i in range(1, 24):
        flags.switches[i]=1


    Input.doy=10;
    Input.year=0; #/* without effect */
    Input.sec=3600; # at 1 UTC
    Input.alt=80; # This will vary
    Input.g_lat=78; # latitude of interest
    Input.g_long=20; # longitude of interest
    Input.lst=4; # local standard time
    Input.f107A=150; #81 day average around date, should be set to 150
    Input.f107=150; # previous day f10.7, should be set to 150
    Input.ap=4; #magnetic activity, should be set to 4


    #evaluate 0 to 14

    gtd7(Input, flags, output)


    #/* output type 1 */

    print('\n', end='')
    for j in range(9):
        print('%E ' % output.d[j], end='')
    print('%E ' % output.t[0], end='')
    print("\nDAY   ", end='')

    print("         %3i" % Input.doy, end='')
    print("\nALT   ", end='')

    print("        %4.0f" % Input.alt, end='')
    print("\nTINF  ", end='')

    print("     %7.2f" % output.t[0], end='')
    print("\nTG    ", end='')

    print("     %7.2f" % output.t[1], end='')
    print("\nHE    ", end='')

    print("   %1.3e" % output.d[0], end='')
    print("\nO     ", end='')

    print("   %1.3e" % output.d[1], end='')
    print("\nN2    ", end='')

    print("   %1.3e" % output.d[2], end='')
    print("\nO2    ", end='')

    print("   %1.3e" % output.d[3], end='')
    print("\nAR    ", end='')

    print("   %1.3e" % output.d[4], end='')
    print("\nH     ", end='')

    print("   %1.3e" % output.d[6], end='')
    print("\nN     ", end='')

    print("   %1.3e" % output.d[7], end='')
    print("\nANM   ", end='')

    print("   %1.3e" % output.d[8], end='')
    print("\nRHO   ", end='')

    print("   %1.3e" % output.d[5], end='')
    print('\n')
        #/* DL omitted */
'''
    #/* output type 2 */
    for i in range(3):
        print('\n', end='')
        print("\nDAY   ", end='')
        for j in range(5):
            print("         %3i" % Input[i*5+j].doy, end='')
        print("\nUT    ", end='')
        for j in range(5):
            print("       %5.0f" % Input[i*5+j].sec, end='')
        print("\nALT   ", end='')
        for j in range(5):
            print("        %4.0f" % Input[i*5+j].alt, end='')
        print("\nLAT   ", end='')
        for j in range(5):
            print("         %3.0f" % Input[i*5+j].g_lat, end='')
        print("\nLONG  ", end='')
        for j in range(5):
            print("         %3.0f" % Input[i*5+j].g_long, end='')
        print("\nLST   ", end='')
        for j in range(5):
            print("       %5.0f" % Input[i*5+j].lst, end='')
        print("\nF107A ", end='')
        for j in range(5):
            print("         %3.0f" % Input[i*5+j].f107A, end='')
        print("\nF107  ", end='')
        for j in range(5):
            print("         %3.0f" % Input[i*5+j].f107, end='')

        print('\n\n', end='')

        print("\nTINF  ", end='')
        for j in range(5):
            print("     %7.2f" % output[i*5+j].t[0], end='')
        print("\nTG    ", end='')
        for j in range(5):
            print("     %7.2f" % output[i*5+j].t[1], end='')
        print("\nHE    ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[0], end='')
        print("\nO     ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[1], end='')
        print("\nN2    ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[2], end='')
        print("\nO2    ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[3], end='')
        print("\nAR    ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[4], end='')
        print("\nH     ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[6], end='')
        print("\nN     ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[7], end='')
        print("\nANM   ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[8], end='')
        print("\nRHO   ", end='')
        for j in range(5):
            print("   %1.3e" % output[i*5+j].d[5], end='')
        print('\n')




'''


if __name__ == '__main__':
    #start = time.clock()
    test2_gtd7()
    #print(time.clock() - start)
