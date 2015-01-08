#!/usr/bin/python
# Tool for concatenating (appending) columns from two files
# Both files need to have the same number of rows in the same order.
# (i.e. Rows A, B, and C should be A, B, and C in both f1 and f2) 
# Provides the option to remove the first column from one file first,
# as this may contain a key value
# Assumes files are tab-delimited
# Double-check all output as some tabs may get lost or duplicated if 
# formatting varies.

remove_first_column = 1

f1 = open("EcoCyc_component_conservation.txt")
f2 = open("EcoCyc_component_conservation_R2.txt")
f3 = open(f1.name + " AND " + f2.name + ".txt", 'w')

if remove_first_column == 1:
	for line in f1:
		f2line = ((f2.readline()).rstrip()).split("\t")
		f2line.pop(0)
		addedline = "\t".join(f2line)
		f3.write(line.rstrip() + addedline + "\n")
else:
	for line in f1:
		f3.write(line.rstrip() + "\t" + f2.readline())
f1.close()
f2.close()
f3.close()
