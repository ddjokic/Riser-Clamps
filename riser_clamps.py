#!/usr/bin/env python
# encoding: utf-8
'''
allrclamp.py

Usage: $ python rclamp.py 
(c) ckunte, 2011

'''
import sys
from bisect import bisect
from math import *
import inout

## Roark's Table 26, Case 10, with three edges fixed
a_by_b = [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00]
b1 = [0.020, 0.081, 0.173, 0.321, 0.727, 1.226, 2.105]
##

# Common design checks applicable to both hanger and sliding clamps.
def sclamp():
	# User input
	
	# User input (keyboard): Applied force and bolts (keyboard)
	F=inout.get_float("Input Expected Maximum Force on the clamp, F [kN] or '0' for 3000 kN: ", 3000)	
	d=inout.get_float("Input Bolt Diameter, d[mm] or '0' for 28 mm: ", 28)
	n=inout.get_integer("Input Number of Bolts or '0' for 8: ", 8)
	Fu=inout.get_float("Input Minimum Tensile Strenght of bolts [MPa] or '0' for 860 MPa (ASTM A193 Gr. B7): ", 860)
	inout.write_file(fn, "Maximum Force on the clamp [MPa]: ", F)
	inout.write_file(fn, "Bolt diameter [mm]: ", d)
	inout.write_file(fn, "Minimum tensile strenght of bolts [MPa]: ", Fu)
	inout.write_file(fn, "Number of bolts: ", n)
	
	# User input (keyboard): Flange plate and yield strength

	bp=inout.get_float("Input Flange plate width [mm] or '0' for 500mm: ",500)
	tf=inout.get_float("Input Flange plate thickness [mm] or '0' for 25mm: ",25)
	ts=inout.get_float("Input Stiffener plate thickness [mm] or '0' for 25mm: ", 25)
	sp=inout.get_float("Input Spacing bitween stiffeners [mm] or '0' for 150mm: ", 150)
	Fy=inout.get_float("Input Yieeld strenght of material [MPa] or '0' for 250 MPa (ASTM A36 steel): ", 250)
	inout.write_file(fn, "Flange plate width [mm]: ", bp)
	inout.write_file(fn, "Flange plate thickness [mm]: ", tf)
	inout.write_file(fn, "Stiffener plate thickness [mm]: ", ts)
	inout.write_file(fn, "Spacing between stiffeners [mm]: ", sp)
	inout.write_file(fn, "Yield Strenght of material [MPa]: ", Fy)
	
	#Additional data
	dris=inout.get_float("Input Riser diameter [mm] or '0' for 150 mm: ",150)
	tnr=inout.get_float("Input Neoprene thickness on riser [mm] or '0' for 15 mm: ", 15)
	g=inout.get_float("Input Air gap in clamp [mm] or '0' for 10 mm: ",10)
	tnc=inout.get_float("Input Neoprene thickness on clamp [mm] or '0' for 10 mm: ", 10)
	tc=inout.get_float("Input Clamp rolled plate thickness [mm] or '0' for 23 mm: ",23)
	inout.write_file(fn, "Riser diameter [mm]: ", dris)
	inout.write_file(fn, "Neoprene thickness on riser [mm]: ", tnr)
	inout.write_file(fn, "Air gap in clamp [mm]: ", g)
	inout.write_file(fn, "Neoprene thickness on clamp [mm]: ",tnc)
	inout.write_file(fn, "Clamp rolled plate thickness [mm]: ",tc)
	
		
	# Stop if any input is < or = to zero.
	while F <= 0 or d <= 0 or n <= 0 or Fu <=0 \
	      or bp <= 0 or tf <= 0 or ts <= 0 or sp <=0 or Fy <=0 \
	      or dris <= 0 or tc <=0:
		print ("Check input, and try again.")
		break
		
	# Continue calculation if input is > zero.
	else:
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
		inout.write_file(fn,"Bolt shear strenght, Va[kN]: ", round(Va,3))
		inout.write_file(fn,"Interaction ratio, V/Va: ", round (IRs,3))
		
		
		# FLANGE PLATE DESIGN CHECK
		
		# Bolt force transmitted is assumed as a uniformly distributed
		# load (UDL). Intensity of UDL (MPa):
		
		q = Ft * 10**3 / ((sp + ts) * bp)
				
		abyb = float(sp + ts) / bp
		
		# To be able to call this in hclamp()
		
		# Find the index number of the ratio abyb in the list a_by_b
		# (e.g., if abyb results in 0.50, then the index number in 
		# the list a_by_b would be 1):
		
		try:
			i = a_by_b.index(abyb)
			print "Index value of the ratio a / b: ", i
			
			# Corresponding values from the column:
			beta1 = b1[i]
			
		except ValueError:
			# Exact match of abyb is not found. So, plan B:
			# find the index number in the list of row a_by_b
			# e.g., if the ratio abyb results in, say, 0.6, then
			# i will be assigned to the appropriate index number
			# in the list a_by_b, which in this case would be
			# equal to 2.
			
			i = bisect(a_by_b, abyb)
			j = i - 1
			print "Index value of the ratio a / b: ", i
			print "j = i - 1: ", j
			
			# Interpolate data to get input for Roark's formula.
			
			A = (b1[i] - b1[j]) 
			b = (abyb - a_by_b[j])
			B = (a_by_b[i] - a_by_b[j])
			
			beta1 =  b1[j] + (A * b / B)
			print "beta1: ", beta1
			
		# sigma_b_max in MPa
		sigma_b_max = -(beta1 * q * bp**2) / (tf**2)
			
		# Allowable bending stress:
		Fb = Fy * 0.75
		
		# Interaction ratio (Shear):
		IRb = sigma_b_max / Fb
		
		# Print results of flange plate design check:
		
		fn.write("\n\nFlange Plate Design Check")
		fn.write("\nRef: Table 26, Case 10, Roark's Formulas.")
		inout.write_file(fn, "Max. bending stress, sigma_b_max [MPa]: ", round(sigma_b_max,3))
		inout.write_file(fn, "Allowable bending stress (0.75.Fy), Fb [MPa]: ", round(Fb,3))
		inout.write_file(fn, "Interaction ratio, sigma_b_max / Fb : ", round(IRb,3))

		# ROLLED PLATE DESIGN CHECK
		
		#Outer diameter of riser clamp (mm):
		OD = dris + 2 * (tnr + g + tnc + tc)
		
		# Hoop stress in rolled plate (MPa):
		fh = Ft * 10**3 / ((sp + ts) * tc)
		
		# Length of the rolled plate:
		L = (n /2) * sp + (n/(2 +1)) * ts
		
		# Geometric parameter (3.2.5-5, API RP-2A):
		M = (L/OD) * sqrt(OD * 2 / tc)
		
		# Hoop Buckling Stress (Cl. 3.2.5b, API RP-2A):
		if M >= (1.6 * OD / tc):
			Ch = tc * 0.44 / OD
		
		if (OD * 0.825 / tc) <= M < (OD * 1.6 / tc):
			Ch = (tc * 0.44 / OD) + (OD / tc)**3 * 0.21 / M**4
		
		if 3.5 <= M < (OD * 0.825 / tc):
			Ch = 0.736 / (M - 0.636)
			
		if 1.5 <= M < 3.5:
			Ch = 0.755 / (M - 0.559)
			
		if M < 1.5:
			Ch = 0.8
			
		# Elastic hoop buckling stress (MPa):
		E = 2 * 10**5 
		Fhe = Ch * 2 * E * tc / OD
		
		# Elastic buckling:
		if Fhe <= (Fy * 0.55):
			Fhc = Fhe
		
		# Inelastic buckling:	
		if (Fy * 0.55) < Fhe <= (Fy * 1.6):
			Fhc = (Fy * 0.45) + (Fhe * 0.18)
		
		if (Fy * 1.6) < Fhe < (Fy * 6.2):
			Fhc = (Fy * 1.31) / ((Fy / Fhe) + 1.15)
		
		if Fhe > (Fy * 6.2):
			Fhc = Fy
			
		FOS = Fhc / fh
		
		# Print results of flange plate design check:
		fn.write("\n\nRolled Plate Design Check")
		fn.write("\nRef: Clause 3.2.5b, API RP-2A.")
		inout.write_file(fn, "Hoop stress in rolled plate, fh [MPa]: ", round(fh,3))
		inout.write_file(fn, "Critical hoop buckling stress, Fhc [MPa]: ", round(Fhc,3))
		inout.write_file(fn, "Safety factor, Fhc/fh: ", round(FOS,3))
		fn.write("\n")
		
	
	# To enable to be called in hclamp()
	global F, Fy, abyb



# Hanger clamp specific checks.
def hclamp():
	# ANNULAR FLANGE PLATE IN HANGER CLAMP
	# User input (keyboard): Rolled plate, neoprene
	Lafp=inout.get_float("Input Length of annular flange plate [mm] or '0' for 500 mm: ",500)
	Bafp=inout.get_float("Input Width of annular flange plate [mm] or '0' for 200 mm: ",200)
	tafp=inout.get_float("Input Thickness of annular flange plate [mm] or '0' for 25 mm: ",25)
	ns=inout.get_integer("Input Number of un-supported sectors of annular plate or '0' for 3: ",3)
	inout.write_file(fn, "Length of annular flange plate [mm]: ",Lafp)
	inout.write_file(fn, "Width of annular flange plate [mm]: ",Bafp)
	inout.write_file(fn, "Thickness of annular flange plate [mm]: ",tafp)
	inout.write_file(fn, "Number of un-supported sectors of annular plate: ", ns)
	if tafp > 0:
		# Load per sector of flange plate (kN):
		Fsec = float(F) / ns
		
		# Intensity of UDL (MPa):
		qafp = Fsec * 10**3 / (Lafp * Bafp)
		
		# To calculate sigma_b_max (Roark's table 26, case 10):
		
		lbyb = float(Lafp) / Bafp
		
		try:
			i = a_by_b.index(lbyb)
			
			# Corresponding values from the column:
			beta1 = b1[i]
			print "beta1: ", beta1
			print "qafp : ", qafp
			
		except ValueError:
			i = bisect(a_by_b, lbyb)
			j = i - 1
			print "Index value of the ratio a / b: ", i
			print "j = i - 1: ", j
			
			# Interpolate data to get input for Roark's formula.
			
			A = (b1[i] - b1[j]) 
			b = (abyb - a_by_b[j])
			B = (a_by_b[i] - a_by_b[j])
			beta1 =  b1[j] + (A * b / B)
			print "beta1: ", beta1
			print "qafp : ", qafp
        
		# sigma_b_max in MPa
		sigma_b_max = beta1 * qafp * Bafp**2 / (tafp**2)
		
		# Allowable bending stress:
		Fb = Fy * 0.75
        
		# Interaction ratio (Shear):
		IRafp = sigma_b_max / Fb
					
		# Print results of flange plate design check:
		
		fn.write("\n\nAnnular Flange Plate Design Check")
		fn.write("\nRef: Table 26, Case 10, Roark's formulas")
		inout.write_file(fn, "Max. bending stress, sigma_b_max [MPa]: ", round(sigma_b_max,3))
		inout.write_file(fn, "Allowable bending stress (0.75.Fy), Fb [MPa]: ", round(Fb,3))
		inout.write_file(fn, "Interaction ratio, sigma_b_max/FB: ",round(IRafp, 3))
		fn.write("\n")
		pass
	
	else:
		print ("Annualar plate thickness cannot be zero for this check.")		
						
	pass
print("Cloned from ckunte's allrclamp.py")
print ("1 - Hanger clamp.")
print ("2 - Sliding clamp.")
choice=inout.get_integer("Choose type of clamp to check - 1 or 2: ",1)
fname='clamps.txt'
if choice==1:
	fn=open(fname, 'a')
	fn.write("\n")
	fn.write("\nHanger Riser Clamp Check")
	fn.write("\n")
	sclamp()
	hclamp()
	fn.close()
	print("Job done - check file 'clamps.txt' for results")
elif choice==2:
	fn=open(fname, 'a')
	fn.write("\n")
	fn.write("\nSliding Raiser Clamp Check")
	fn.write("\n")
	sclamp()
	fn.close()
else:
	print("Wrong Input - try again!")
	fn.close()
	print("Job done - check file 'clamps.txt' for results")
