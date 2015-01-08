#!/usr/bin/python
# Script for converting spicednog-marshmallow-simple output to fractional conservation for
# each complex in a set of complexes.
# INPUTS: A matrix of conservation per species, with one species per row and 
# one OG per column. A second file contains a list of complexes and their OG components.
# OUTPUT: A matrix like the first input file, but with one complex per column.
# Output values are fractional conservation (that is, (# conserved vs. ref)/(# of components in ref. complex))
# Still a little messy.

import sys, array

conlist = open("EcoCyc_and_Hu_complex_component_conservation.txt")
complexlist = open("Hu_E_coli_complexes.txt")
fractionsf = open('Hu_complex_conservation_fractions.txt', 'w')

#Load all the complexes, storing components in one list and names in another
#They should all remain in the same order though
allcomplexes = []
allnames = []
for line in complexlist:
	singlecomplex = (line.rstrip()).split("\t")
	singlename = singlecomplex.pop(0)
	allcomplexes.append(singlecomplex)
	allnames.append(singlename)
#print(allcomplexes)

#Load all components we have conservation for - list includes first column for consistency
possiblecomponents = ((conlist.readline()).rstrip()).split("\t")
print("Using conservation of " + str(len(possiblecomponents)) + " components in " + str(len(allnames)) + " complexes.")

#Check to make sure the data matches up
missingcount = 0
missingcomponents = []
for itercomplex in allcomplexes:
	for component in itercomplex:
		if component in possiblecomponents:
			continue
			#print(component + " is in the set.")
		else:
			#print(component + " is NOT IN THE SET.")
			missingcomponents.append(component)
			missingcount = missingcount +1
if missingcount > 0:
	print(str(missingcount) + " components are missing in the conservation data.")
	print(missingcomponents)

#Set up the output file
allnames.insert(0,"Species")
fractionsf.write("\t".join(allnames) + "\n")

#Iterate through all species and complexes
errors = 0 #The number of components which couldn't be found in the set
for line in conlist:
	line = (line.rstrip()).split("\t")
	fractionsf.write(line[0] + "\t")
	for itercomplex in allcomplexes:
		totalcon = 0
		for component in itercomplex:
			try:
				whichone = possiblecomponents.index(component)
				totalcon = totalcon + int(line[whichone])
				#print(totalcon)
			except ValueError:
				errors = errors +1
				#print("Can't find " + component + " in the search set!")
		fractioncon = (totalcon / float(len(itercomplex)))
		fractionsf.write(str(fractioncon) + "\t")
		#if fractioncon:
			#print("%s\t%s\t%s\t%s") % (line[0], itercomplex, totalcon, len(itercomplex))
		#fractionsf.write(repr(fractioncon))
		#print(line[0] + "\t" + str(fractioncon))
	fractionsf.write("\n")
print("Wrote output to " + fractionsf.name)

