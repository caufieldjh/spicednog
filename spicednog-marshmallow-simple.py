#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# OG presence helper - simple version
# Needs to be placed in same directory as *.members.txt (usually /all.members)
# Input: As an input text file, the name of one or more eggNOG OGs (i.e., COG1234).
# 	COGs, NOGs, and bactNOGs will work.
# Output: A taxon ID number and presence or absence of the OG for that taxon.
#	1 indicates the OG is present at least once for that taxon ID.
#	0 indicates the OG could not be found for that taxon ID.
# At the moment this is set up to write to my Dropbox, 
# so if you aren't Harry then you should change that.

import sys, array

#specieslist = open("speclist-edited.txt")  
specieslist = open("speclist-big.txt") #This is just a list of NCBI taxon IDs (Also used by eggNOG), one on each line.
searchlist = open("HuComplexComponentsWithoutEC.txt")
listOfSpec = []
listOfOG = []
searchOGs = []

if (len(sys.argv)>1):
	for eacharg in sys.argv:
		searchOGs.append(eacharg)
	del searchOGs[0]
	#print "Searching for %s OGs in total." % len(searchOGs)
else:
	for line in searchlist:
		searchOGs.append(line.rstrip())
resultsList = [0]

#Set up the arrays of species and OGs to search.
for line in specieslist:
	listOfSpec.append(line.rstrip())
specieslist.close()
if any("COG" in item for item in searchOGs):
	coglist = open("COG.members.txt")
	for line in coglist:
		listOfOG.append(line)
	#print "Loaded COG list."
	coglist.close()
if any("bactNOG" in item for item in searchOGs):
	bactnoglist = open("bactNOG.members.txt")
	for line in bactnoglist:
		listOfOG.append(line)
	#print "Loaded bactNOG list."
	bactnoglist.close()	
if any("NOG" in item for item in searchOGs):
	noglist = open("NOG.members.txt")
	for line in noglist:
		listOfOG.append(line)
	#print "Loaded NOG list."
	noglist.close()

for eachOG in searchOGs:
	print "Searching for %s..." % eachOG
	resultsLine = -1
	oneSpeciesResults = []
	for i in listOfSpec:
		resultsLine = resultsLine +1
		positivecount = 0
		for jline in listOfOG:
			if i in jline and eachOG in jline:
				positivecount = 1
				#print "%s found in %s" % (eachOG, i)
				break
		#print "%s\t%s" % (i, positivecount)
		oneSpeciesResults.append(positivecount)
		#print oneSpeciesResults
	resultsList.append(oneSpeciesResults)

marshmallow_out=open('C:\Users\Harry\Dropbox\Marshmallow_output.txt', 'w')			
marshmallow_out.write("*Species*\t%s" % '\t'.join(map(str, searchOGs)) + "\n")
index = 0
for item in listOfSpec:
	tempString = "%s\t" % item
	index2 = 1
	for OG in searchOGs:
		tempString = tempString + "\t" + str(resultsList[index2][index])
		index2 = index2 +1
	marshmallow_out.write(tempString + "\n")
	index = index +1
	#On the same line, print the corresponding results row
