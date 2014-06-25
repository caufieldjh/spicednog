#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# OG presence helper
# Needs to be placed in same directory as *.members.txt (usually /all.members)
# Input: At the command line, the name of one or more eggNOG OGs (i.e., COG1234)
# 	COGs or NOGs will work but other sublevels will not (yet).
# Output: A taxon ID number and the number of members of the specified OG its genome contains.


import sys, array

specieslist = open("eDUFspeclist.txt")
#specieslist = open("speclist-edited.txt") #This is just a list of NCBI taxon IDs (Also used by eggNOG), one on each line. 
#specieslist = open("tempspeclist.txt")
coglist = open("COG.members.txt")
noglist = open("NOG.members.txt")
listOfSpec = []
listOfOG = []
searchOGs = []

if (len(sys.argv)>1):
	for eacharg in sys.argv:
		searchOGs.append(eacharg)
	del searchOGs[0]
	print "Searching for %s OGs in total." % len(searchOGs)
else:
	sys.exit("No OGs provided.")
resultsList = [0]

#Set up the arrays of species and OGs to search.
for line in specieslist:
	listOfSpec.append(line.rstrip())
specieslist.close()
if any("COG" in item for item in searchOGs):
	for line in coglist:
		listOfOG.append(line)
	print "Loaded COG list."
	coglist.close()
if any("NOG" in item for item in searchOGs):
	for line in noglist:
		listOfOG.append(line)
	print "Loaded NOG list."
	noglist.close()

for eachOG in searchOGs:
	print "Searching for %s" % eachOG
	resultsLine = -1
	oneSpeciesResults = []
	for i in listOfSpec:
		resultsLine = resultsLine +1
		positivecount = 0
		for jline in listOfOG:
			if i in jline and eachOG in jline:
				positivecount = positivecount + 1
		print "%s\t%s" % (i, positivecount)
		oneSpeciesResults.append(positivecount)
		#print oneSpeciesResults
	resultsList.append(oneSpeciesResults) 
			
print "*Species*\t%s" % '\t'.join(map(str, searchOGs))
index = 0
for item in listOfSpec:
	tempString = "%s\t" % item
	index2 = 1
	for OG in searchOGs:
		tempString = tempString + "\t" + str(resultsList[index2][index])
		index2 = index2 +1
	print tempString
	index = index +1
	#On the same line, print the corresponding results row
