#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# OG presence helper - simple version
# Updated to work with eggNOG v.4
# Needs to be placed in same directory as the following eggNOG v.4 *.members.tsv files:
#  bactNOG.members.tsv
#  NOG.members.tsv
# These files are available at http://eggnogdb.embl.de/#/app/downloads
# Input: * As an input text file, the name of one or more eggNOG OGs (i.e., ENOG4105ZRE).
#	* An an additional input, a file containing a list of 
#		NCBI taxon IDs (Also used by eggNOG), one on each line
# Output: A taxon ID number and presence or absence of the OG for that taxon.
#	1 indicates the OG is present at least once for that taxon ID.
#	0 indicates the OG could not be found for that taxon ID.

import array, re, sys

specieslist = open("speclist.txt") #The species list to use
searchlist = open("test_ogs.txt")
listOfSpec = []
listOfOG = []
searchOGs = []

output_filename = "marshmallow_output.txt"

def main():
	if (len(sys.argv)>1):
		for eacharg in sys.argv:
			searchOGs.append(eacharg)
		del searchOGs[0]
		print "Searching for %s OGs in total." % len(searchOGs)
	else:
		for line in searchlist:
			searchOGs.append(line.rstrip())
			
	resultsList = {}
	
	#Set up the arrays of species and OGs to search.
	for line in specieslist:
		listOfSpec.append(line.rstrip())
	specieslist.close()
	
	with open("NOG.members.tsv") as noglist:
		for line in noglist:
			split_line = (line.rstrip()).split("\t")
			parsed_line = split_line[:5]
			parsed_line.append(re.split('[,.]',split_line[5]))
			listOfOG.append(parsed_line)
		print "Loaded NOG list."
	
	with open("bactNOG.members.tsv") as bactnoglist:
		for line in bactnoglist:
			split_line = (line.rstrip()).split("\t")
			parsed_line = split_line[:5]
			parsed_line.append(re.split('[,.]',split_line[5]))
			listOfOG.append(parsed_line)
		print "Loaded bactNOG list."
	
	for eachOG in searchOGs:
		print "Searching for %s..." % eachOG
		oneSpeciesResults = {}
		for group in listOfOG:
			if group[1] == eachOG:
				for i in listOfSpec:
					if i in group[5]:	
						oneSpeciesResults[i] = 1
					else:
						oneSpeciesResults[i] = 0
				break
		resultsList[eachOG] = oneSpeciesResults
	
	marshmallow_out=open(output_filename, 'w')			
	marshmallow_out.write("*Species*\t%s" % '\t'.join(map(str, searchOGs)) + "\n")
	index = 0
	for taxid in listOfSpec:
		tempString = "%s\t" % taxid
		for og in searchOGs:
			tempString = tempString + str(resultsList[og][taxid]) + "\t"
		marshmallow_out.write(tempString.rstrip() + "\n")
		index = index +1
		#On the same line, print the corresponding results row
	print("Complete. See %s for conservation matrix." % output_filename)
	
if __name__ == "__main__":
	sys.exit(main())
