#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# convert module - for turning Uniprot IDs into other things
# Works properly when in same directory as the following:
#	protein.aliases.v3.txt	
#	Extracted "all.members.tar.gz" 
# Optimized for bacteria.
#INPUT: A list of Uniprot IDs, one per line, in file
import mmap, re, sys, string, os

# Define input files
filenameAliases = "protein.aliases.v3.txt"
filenameCOG = "all.members/COG.members.txt"
filenameNOG = "all.members/NOG.members.txt"
filenamebactNOG = "all.members/bactNOG.members.txt"

# prompt for upids
if (len(sys.argv)>1):
	#print str(sys.argv[1])
	filenameupid = str(sys.argv[1])
else:
	print("Please enter Uniprot ID list file")
	filenameupid = input("> ")
idfile = open(filenameupid)
print("upid\tlocus\tcogID\tnogID\tbactnogID")

# Search the input file for matching rows.
#Just returns the first matching hit.
undefinedvar = 'undefined'
for line in idfile:
	upid = line.rstrip()
	#print("***NOW SEARCHING ALIAS FILE FOR LOCUS FOR " + upid + "***")
	txt = open(filenameAliases)
	for line in txt:
		#print line
		locusline = undefinedvar
		if upid in line:
			locusline = line
			#print line
			break
		if locusline is undefinedvar:
			locus = locusline
	locuslist=locusline.split("|")
	locus = locuslist[0]
	#print locus
# Move on to the COG and NOG files		
	txt.seek(0,0)
	
## Retrieve rows from OG files with the corresponding species code. Write to the same output file
	cogID = "NA"
	nogID = "NA"
	bactnogID = "NA"
	txt2 = open(filenameCOG)
	#print("***NOW SEARCHING COG FILE FOR LOCUS FOR " + upid + "***")
	for line in txt2:
		if locus is undefinedvar:
			break
		if locus in line:
			#print line
			cogID = line[0:7]
			break
	txt2.close()
	txt3 = open(filenameNOG)
	#print("***NOW SEARCHING NOG FILE FOR LOCUS FOR " + upid + "***")
	for line in txt3:
		if locus is undefinedvar:
			break
		if locus in line:
			#print line
			nogID = line[0:8]
			break
	txt3.close()
	txt4 = open(filenamebactNOG)
	#print("***NOW SEARCHING bactNOG FILE FOR LOCUS FOR " + upid + "***")
	for line in txt4:
		if locus is undefinedvar:
			break
		if locus in line:
			#print line
			bactnogID = line[0:12]
			break
	txt4.close()
	print(upid + "\t" + locus + "\t" + cogID + "\t" + nogID + "\t" + bactnogID)
# Output everything, one line each ID

sys.exit(0)
