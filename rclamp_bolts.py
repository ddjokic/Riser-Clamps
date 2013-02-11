#!/usr/bin/env python
import sys
from math import *
import inout
print("Cloned from ckunte's allrclamp.py")
print("Calculating Bolts of riser clamps")
fname="clamps-bolting.txt"
fn=open(fname, 'a')
#input block
F=inout.get_float("Input Expected Maximum Force on the clamp, F [kN] or '0' for 3000 kN: ", 3000)	
d=inout.get_float("Input Bolt Diameter, d[mm] or '0' for 28 mm: ", 28)
n=inout.get_integer("Input Number of Bolts or '0' for 8: ", 8)
Fu=inout.get_float("Input Minimum Tensile Strength of bolts [MPa] or '0' for 860 MPa (ASTM A193 Gr. B7): ", 860)
inout.write_file(fn, "Maximum Force on the clamp [MPa]: ", F)
inout.write_file(fn, "Bolt diameter [mm]: ", d)
inout.write_file(fn, "Minimum tensile strength of bolts [MPa]: ", Fu)
inout.write_file(fn, "Number of bolts: ", n)

#calculation
# CHECK FOR TENSION IN BOLTS
		
# Axial force per bolt (in kN):
Fa = float(F) / n

# Tensile stress area per bolt (in mm^2):
At = pi * d**2 / 4

# Allowable tension (in kN):
Ft = Fu * At / (3 * 10**3)

# Interaction ratio (Tension):
IRt = Fa / Ft
		
# Print results of tension check in bolts:
fn.write("\n\nBolts Tension Check")
fn.write("\nRef: Clause J3.4, and Table J3.2, AISC.")
inout.write_file(fn, "Axial force per bolt, Fa[kN]: ", round(Fa,3))
inout.write_file(fn, "Tensile stress area of bolt, At[mm**2]: ",round(At,3))
inout.write_file(fn, "Allowable tension, Ft[kN]: ",round(Ft,3))
inout.write_file(fn, "Interaction ratio, Fa/Ft: ", round(IRt,3))

# CHECK FOR SHEAR IN BOLTS

# Direct shear:
V = float(F) / n

# Shear strength of bolt:
Va = Fu * At * 0.17 / 10**3

# Interaction ratio (Shear):
IRs = V / Va

# Print results of shear check in bolts:
fn.write("\n\nBolts Shear Check")
fn.write("\nRef: Table J3.2, AISC.")
inout.write_file(fn,"Maximum shear force. F[kN]: ", round(F,3))
inout.write_file(fn,"Direct shear, V[kN]: ", round(V,3))
inout.write_file(fn,"Bolt shear strength, Va[kN]: ", round(Va,3))
inout.write_file(fn,"Interaction ratio, V/Va: ", round (IRs,3))