#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# Bacterial Conservation helper
# For internal use only! 
# Gets average locus and OG conservation values when given an input file.
# Needs the big list of OG conservation first.

import mmap, re, sys, string, os

# Define input files
filenameBacCon = "AllBacConUniq.txt"

# print "The species file is %r:" % filenameSpecies
print "Please input the filename of the locus list to be used."
if (len(sys.argv)>1):
	print str(sys.argv[1])
	filenameLoci = str(sys.argv[1])
else:
	filenameLoci = raw_input("> ")

bacConValues = open(filenameBacCon)
rawLoci = open(filenameLoci)

countLoci = 0
countOG = 0
lociConSum = 0
ogConSum = 0
previousOG = "NULL"
listOfBacConValues = []
for line in bacConValues:
	listOfBacConValues.append(line)
bacConValues.close()
listOfLoci = []
for line in rawLoci:
	listOfLoci.append(line)
rawLoci.close()

for j in listOfLoci:
	j = j.split()
	thisOG = j[0]
	for i in listOfBacConValues:
		if thisOG in i:
			i = i.split()
			oneConValue = float(i[1])
			lociConSum = lociConSum + oneConValue
	if thisOG != previousOG:
		ogConSum = ogConSum + oneConValue
		countOG = countOG + 1
	countLoci = countLoci + 1
	#percentComplete = (countLoci / float((len(listOfLoci)))) * 100
	#if (percentComplete - int(percentComplete)) < 0.01:
		#print "%s percent complete" % int(percentComplete)
	previousOG = thisOG
	
lociConAverage = lociConSum / countLoci 
ogConAverage = ogConSum / countOG 

print "*For %s:" % filenameLoci
#print "Total loci: %s" % (countLoci)
#print "Total OGs: %s" % (countOG)
print "Average loci conservation: %s" % (lociConAverage/943)
print "Average OG conservation: %s" % (ogConAverage/943)
sys.exit(0)
