SPICEDNOG
=========
SPecIfic Conservation for Every DamN Orthologous Group
Intended for parsing and retrieving data from the eggNOG project (v.3) flat files.
(See http://eggnog.embl.de/version_3.0/)
SPICEDNOG is intended for use with bacterial genomes and bacterial gene orthology.
There are four components:
spicednog.py takes a species or strain name and provides lists of genes, orthologous groups, and basic counts of locus types.
spicednog-baccon.py gets average locus and OG conservation values when given an input file of species IDs.
spicednog-convert.py takes lists of Uniprot IDs and converts them into OG, NOG, and bactNOG IDs if available.
spicednog-marshmallow.py takes an OG ID and finds genomes which contain it.
