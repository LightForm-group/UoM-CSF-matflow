from odbAccess import *
from abaqusConstants import *
import sys

ODBaOuvrir = 'myjob.odb'

# Open the .odb, the assembly and the instance
myOdb = openOdb(path=ODBaOuvrir)
myAssembly = myOdb.rootAssembly
myInstance = myAssembly.instances["MK_SAMPLE-1"]

# Frames of the step
frames = myOdb.steps["Step-1"].frames

###################################################
###################################################

# File where the results will be written
Data = open("results_num.dat",'w+') 

# Element sets
Mid_el = myAssembly.elementSets["MIDDLE_ELEMENT"]
Corner_el = myAssembly.elementSets["CORNER_ELEMENT"]

Data.write("%time, S_mid_mises,  LE_mid_mises,  LE_mid_11,  LE_mid_22,  S_corner_mises,  LE_corner_mises,  LE_corner_11,  LE_corner_22\n")

for t in range(len(frames)):
    # Time
    maFrame = frames[t]	
    timeMF = maFrame.frameValue
    # Stress
    Stress = maFrame.fieldOutputs['S']
    Stress_mid = Stress.getSubset(region=Mid_el,position=CENTROID).values
    Stress_corner = Stress.getSubset(region=Corner_el,position=CENTROID).values
    # Strain
    Strain = maFrame.fieldOutputs['LE']
    Strain_mid = Strain.getSubset(region=Mid_el,position=CENTROID).values
    Strain_corner = Strain.getSubset(region=Corner_el,position=CENTROID).values
        
    for el in range(len(Stress_mid)):
        S_mid_mises = Stress_mid[el].mises
        LE_mid_mises = Strain_mid[el].mises
        LE_mid_11 = Strain_mid[el].data[0]        
        LE_mid_22 = Strain_mid[el].data[1]           
        
        S_corner_mises = Stress_corner[el].mises
        LE_corner_mises = Strain_corner[el].mises
        LE_corner_11 = Strain_corner[el].data[0]        
        LE_corner_22 = Strain_corner[el].data[1]      
        
        # Writing
        Data.write(" ")
        Data.write(str(timeMF))
        Data.write(" ")
        Data.write(str(S_mid_mises))
        Data.write(" ")
        Data.write(str(LE_mid_mises))
        Data.write(" ")
        Data.write(str(LE_mid_11))
        Data.write(" ")
        Data.write(str(LE_mid_22))
        Data.write(" ")
        Data.write(str(S_corner_mises))
        Data.write(" ")
        Data.write(str(LE_corner_mises))
        Data.write(" ")
        Data.write(str(LE_corner_11))
        Data.write(" ")
        Data.write(str(LE_corner_22))
        Data.write("\n")

Data.close()

###################################################
###################################################

# File where the results of all nodes will be written
Data = open("results_num_all.dat",'w+') 

# All elements
All_el = myInstance.elementSets["SHEET_ELEMENTS"]

Data.write("%time, S_mises,  LE_mises,  LE_11,  LE_22, X, Y, Z\n")

for t in range(len(frames)):
    # Time
    maFrame = frames[t]	
    timeMF = maFrame.frameValue
    # Stress
    Stress = maFrame.fieldOutputs['S']
    Stress_all = Stress.getSubset(region=All_el,position=CENTROID).values
    # Strain
    Strain = maFrame.fieldOutputs['LE']
    Strain_all = Strain.getSubset(region=All_el,position=CENTROID).values
	# Coord
    COR=maFrame.fieldOutputs['COORD']
    CORfieldValues=COR.getSubset(region=All_el,position=CENTROID).values
        
    for el in range(len(Stress_all)):
		S_all_mises = Stress_all[el].mises
		LE_all_mises = Strain_all[el].mises
		LE_all_11 = Strain_all[el].data[0]        
		LE_all_22 = Strain_all[el].data[1]           
		COOR1=CORfieldValues[el].data[0]
		COOR2=CORfieldValues[el].data[1]	
		COOR3=CORfieldValues[el].data[2]

		# Writing
		Data.write(" ")
		Data.write(str(timeMF))
		Data.write(" ")
		Data.write(str(S_all_mises))
		Data.write(" ")
		Data.write(str(LE_all_mises))
		Data.write(" ")
		Data.write(str(LE_all_11))
		Data.write(" ")
		Data.write(str(LE_all_22))
		Data.write(" ")
		Data.write(str(COOR1))
		Data.write(" ")
		Data.write(str(COOR2))
		Data.write(" ")
		Data.write(str(COOR3))
		Data.write("\n")

Data.close()
