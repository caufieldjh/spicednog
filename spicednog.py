#!/usr/bin/python
# SPecIfic Conservation for Every DamN Orthologous Group - SPICEDNOG 
# For parsing eggNOG files on a single-species or strain basis.
# Works properly when in same directory as the following:
#	species.v3.txt	
#	Extracted "all.members.tar.gz" 
# Optimized for bacteria.
#INPUT: name of desired species or eggNOG identifier. Can enter as command line argument or when prompted

import mmap, re, sys, string, os

# Define input files
filenameSpecies = "species.v3.txt"
filenameCOG = "all.members/COG.members.txt"
filenameNOG = "all.members/NOG.members.txt"
filenamebactNOG = "all.members/bactNOG.members.txt"

# Open the species file and prompt for species name
txt = open(filenameSpecies)
# print "The species file is %r:" % filenameSpecies
print "Which species are you looking for?"
if (len(sys.argv)>1):
	print str(sys.argv[1])
	speciesname = str(sys.argv[1])
else:
	speciesname = raw_input("> ")

# Search the species file for matching rows, get species code and display them
speciesmatches = 0
print txt.readline()
for line in txt:
	if re.search(speciesname, line):
		speciescode = re.match('[0-9]{4,}', line)
		if re.search("core species", line):
			bestspeciescode = speciescode
		speciesmatches = speciesmatches + 1
		print line,

# If there is one match, use that one. If there are >1 matches, allow the user to choose by species code
if speciesmatches != 0:
	if speciesmatches == 1:
		print "Your species code is %r." % speciescode.group()
		speciescode = speciescode.group()
	else:
		try: 
			bestspeciescode
		except NameError:
			print "More than one entry was matched. Aborting this run."
			sys.exit(0)
		else:
			speciescode = bestspeciescode
		print "There were %s matches. Your species code may be %s." % (speciesmatches, speciescode.group())
		print "If that is acceptable, enter Y. If not, type your chosen species code (the first number)."
		if (len(sys.argv)>1):				#For automation purposes. Otherwise will wait for input when 4-digit codes used
			confirms = "Y"
		else:
			confirms = raw_input("> ")
		if confirms == "Y":
			speciescode = speciescode.group()	
		else:
			speciescode = confirms
else: 
	sys.exit("There were no matches. This is how things go sometimes.")

# Go back and get one species (row) entry in case a new one was specified 
# Retrieve its name and total number of loci
txt.seek(0)
for line in txt:
	if re.match(speciescode + '\s', line):
		speciesFullName = re.search('[A-Z]{1}[a-z]+\s[a-z]+( \w+)?( \w+)?', line)
		speciesAllLoci = float((re.search('[0-9]+$', line)).group())
		print "Species name: %s. Number of loci: %s." % (speciesFullName.group(), '{:g}'.format(speciesAllLoci))
		
# Move on to the COG and NOG files		
txt.close()
ogfile=open(speciesFullName.group() + ' OGs.txt', 'w+')
print "\nOK. Building lists..."

# Retrieve rows from OG files with the corresponding species code. Write to the same output file
# Also populate the list of bacterial species while we have that bactNOG file open
loci = 0
bactnogloci = 0
txt2 = open(filenameCOG)
for line in txt2:
	if re.search("\t" + speciescode + "\.\w+", line):
		#print line
		loci = loci + 1
		ogfile.write(line),
txt3 = open(filenameNOG)
for line in txt3:
	if re.search("\t" + speciescode + "\.\w+", line):
		#print line
		loci = loci + 1
		ogfile.write(line),
txt4 = open(filenamebactNOG)
listOfBacteria = [0]			#To be a bacterial species, a code must be used with at least one bactNOG.
for line in txt4:
	if (re.search('\t[0-9]{4,}\.', line)):
		#print (re.search('(?:\t)([0-9]{4,})(?:\.)', line)).group(1)
		listOfBacteria.append(re.search('(?:\t)([0-9]{4,})(?:\.)', line).group(1))
	if re.search("\t" + speciescode + "\.\w+", line):
		#print line
		bactnogloci = bactnogloci + 1
		ogfile.write(line),
setOfBacteria = (set(listOfBacteria))
if (bactnogloci>0):	
	print "This is one of 943 bacterial species/strains in the database."
else:
	print "This is not a bacterial species."
	sys.exit(0)	#This is just here for automation purposes. Comment out when using non-bacteria
ogfile.seek(0)
#for line in ogfile:
	#print line
print "\nSee %s for the OG list." % (ogfile.name)

# Get the number of times each OG is present - a rough analog for paralogy. Duplicates are removed. 
# print "Looking at OGs in %s" % (ogfile.name)
#Buggy right now
ogfileogcounts=open(speciesFullName.group() + ' OG counts.txt', 'w')
with ogfile as f:
	filesize = os.path.getsize(speciesFullName.group() + ' OGs.txt')
	data = mmap.mmap(f.fileno(), filesize)
	#while True:
		#lineline = data.readline()
		#if lineline == "": break
		#print lineline
	allOGlist = re.findall('[C|N]OG[0-9]{4,6}', data)
	allOGset = (set(allOGlist))
	if allOGset:
		for i in allOGset:
			countOG = len(re.findall(i, data))
			ogcountline = "\n" + i + "\t" + str(countOG)
			#print ogcountline
			ogfileogcounts.write(ogcountline),
print "\nSee %s for the OG counts." % (ogfileogcounts.name)
ogfileogcounts.close()

# Get the number of times each locus is present - shows which loci are in >1 OG.
# raw_input("\nPress Enter to see how many times each locus is present.")
#Buggy right now - calculating correctly, just not writing every line?
ogfilelocicounts=open(speciesFullName.group() + ' loci counts.txt', 'w')
alllocilist = re.findall(speciescode + '\.\w+', data)
alllociset = (set(alllocilist))		
if alllociset:
	for i in alllociset:
		countlocus = len(re.findall(i, data))
		locuscountline = "\n" + i + "\t" + str(countlocus)
		#print locuscountline 
		ogfilelocicounts.write(locuscountline),
print "\nSee %s for the locus counts." % (ogfilelocicounts.name)
ogfilelocicounts.close()
		
print "\n* Within %s there are %s loci which map to OGs. %s loci are unique (that is, they don't share OGs)." % (speciesFullName.group(), loci, len(alllociset))
if bactnogloci >1:
	print "* There are %s highest-level OGs and %s bactNOG loci." % ((len(allOGset) - bactnogloci), bactnogloci)
else:
	print "* There are %s OGs." % (len(allOGset))		
print "* OG loci, including any level of NOGs, comprise %s of all loci for this entry. %s loci did not map to OGs." % (('{:.2%}'.format(len(alllociset) / speciesAllLoci)),'{:g}'.format(speciesAllLoci - len(alllociset)))
print "In summary: /| %s | %s | %s | %s |/" % (speciesFullName.group(), speciescode, '{:g}'.format(speciesAllLoci), len(alllociset))

#print "\nPress Enter to get OG conservation across the whole database,\n\ttype B to restrict the search to Bacteria,\n\tOR type X to exit."
#confirms2 = raw_input("> ")
print "Moving on to the bacterial conservation search."
confirms2 = "B"
if confirms2 == "X":
	sys.exit("Bye!")
	
#If requested, open up the COG and NOG and bactNOG files, split by species and remove duplicates, then search for all OGs found above
#If just looking at bacterial conservation, retrieves only OGs from bacterial species.
print "\nOK, searching. This may take a while."
if confirms2 == "B":
	ogfileAllConserve=open(speciesFullName.group() + ' conservation across Bacteria.txt', 'w')
else:
	ogfileAllConserve=open(speciesFullName.group() + ' conservation across the database.txt', 'w')
cogs = mmap.mmap(txt2.fileno(), 0, prot=mmap.PROT_READ)
cogs = re.split('\..+(\n|\Z)', cogs)
cogset = (set(cogs))
if confirms2 == "B":
	filteredcogset = set([])
	for i in cogset:
		if re.search('(?:\t)([0-9]{4,})', i):
			if re.search('(?:\t)([0-9]{4,})', i).group(1) in setOfBacteria:
				filteredcogset.add(i)
	cogset = filteredcogset
	print "Filtered COGs for bacteria only."
cogsettogether = '\t'.join(cogset)
nogs = mmap.mmap(txt3.fileno(), 0, prot=mmap.PROT_READ)
nogs = re.split('\..+(\n|\Z)', nogs)
nogset = (set(nogs))
if confirms2 == "B":
	filterednogset = set([])
	for i in nogset:
		if re.search('(?:\t)([0-9]{4,})', i):
			if re.search('(?:\t)([0-9]{4,})', i).group(1) in setOfBacteria:
				filterednogset.add(i)
	nogset = filterednogset
	print "Filtered NOGs for bacteria only."
nogsettogether = '\t'.join(nogset)
bactnogs = mmap.mmap(txt4.fileno(), 0, prot=mmap.PROT_READ)
bactnogs = re.split('\..+(\n|\Z)', bactnogs)		#Saves time by not filtering bactNOGs - they're already just in bacteria
bactnogset = (set(bactnogs))
bactnogsettogether = '\t'.join(bactnogset)
allOGlistCon = re.findall('[a-z]*[A-Z]{3}[0-9]{4,6}', data) #Get all the OGs for our chosen species.
print "Got all the OGs for the target species."
#print allOGlistCon 
allOGsetCon = (set(allOGlistCon))
#print allOGsetCon
if allOGsetCon:
	for i in allOGsetCon:
		countOG = 0
		if 'COG' in i:
			countOG = (len(re.findall(i + '\t[0-9]+', cogsettogether))) #Finds one instance of the OG per species code.
			ogcountline = "\n" + i + "\t" + str(countOG)
			ogfileAllConserve.write(ogcountline),
		if 'bactNOG' in i:
			countOG = (len(re.findall(i + '\t[0-9]+', bactnogsettogether))) #Ditto. 
			ogcountline = "\n" + i + "\t" + str(countOG)
			ogfileAllConserve.write(ogcountline),	
		if 'NOG' in i and not 'bactNOG' in i:
			countOG = (len(re.findall(i + '\t[0-9]+', nogsettogether))) #Same here. Leaves out missing ones to avoid double-counting bactNOGs
			ogcountline = "\n" + i + "\t" + str(countOG)
			ogfileAllConserve.write(ogcountline),
print "\nSee %s for the OG counts." % (ogfileAllConserve.name)
sys.exit(0)
