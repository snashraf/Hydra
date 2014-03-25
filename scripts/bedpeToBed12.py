#!/usr/bin/env python
import sys
import getopt
import string
from optparse import OptionParser


class BEDPE (object):
	
	def __init__(self, bedList):
		self.c1 = bedList[0]
		self.s1 = int(bedList[1])
		self.e1 = int(bedList[2])
		self.c2 = bedList[3]
		self.s2 = int(bedList[4])
		self.e2 = int(bedList[5])
		self.name = bedList[6]
		self.score = bedList[7]
		self.o1 = bedList[8]		
		self.o2 = bedList[9]


def bedpeToBlockedBed(bedpe, dist):
	
	if bedpe.o1 == "+" and bedpe.o2 == "-": color = "153,0,0"   # deletion breakpoints are red
	elif bedpe.o1 == "-" and bedpe.o2 == "+": color = "0,102,0" # duplication breakpoints are green
	elif bedpe.o1 == "+" and bedpe.o2 == "+": color = "0,51,204"    # inversion breakpoints are blue
	elif bedpe.o1 == "-" and bedpe.o2 == "-": color = "0,51,204"    # inversion breakpoints are blue
	elif bedpe.o1 == "." and bedpe.o2 == "-": color = "0,0,0"   # orphan breakpoints are black
	elif bedpe.o1 == "." and bedpe.o2 == "+": color = "0,0,0"    # orphan breakpoints are black
	
	# are we dealing with an orpanh breakpoint?
	if (bedpe.o1 == "." or bedpe.o2 == "."):
		# handle which end is orphaned
		if bedpe.o2 == "+":
			print bedpe.c2 + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + \
			bedpe.name + "," + bedpe.score + ":" + bedpe.o1 + "/" + bedpe.o2 + \
			":orphan:" + str(abs(bedpe.e2-bedpe.s2)) + "\t" + \
			str(abs(bedpe.e2-bedpe.s2)) + "\t" + \
			"+" + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + color + "\t" + "2" + "\t" + \
			str(bedpe.e2-bedpe.s2) + "," + "1" + "\t" +\
			"0," + str(bedpe.e2 - bedpe.s2+499)
		else:
			print bedpe.c2 + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + \
			bedpe.name + "," + bedpe.score + ":" + bedpe.o1 + "/" + bedpe.o2 + \
			":orphan:" + str(abs(bedpe.e2-bedpe.s2)) + "\t" + \
			str(abs(bedpe.e2-bedpe.s2)) + "\t" + \
			"-" + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + color + "\t" + "2" + "\t" + \
			"1," + str(bedpe.e2-bedpe.s2) + "\t" +\
			"0," + str(500)
	# both ends are aligned
	elif (bedpe.c1 == bedpe.c2) and (abs(bedpe.e2-bedpe.s1) <= dist):

		print bedpe.c1 + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e2) + "\t" + \
		bedpe.name + "," + bedpe.score + ":" + bedpe.o1 + "/" + bedpe.o2 + \
		":intra:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e2) + \
		"\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
		"+" + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e2) + "\t" + color + "\t" + "2" + "\t" + \
		str(bedpe.e1 - bedpe.s1) + "," +  str(bedpe.e2 - bedpe.s2) + "\t" + \
		"0," +	str(bedpe.s2- bedpe.s1)
	
	# intrachromosomals that exceed dist
	elif (bedpe.c1 == bedpe.c2) and (abs(bedpe.e2-bedpe.s1) > dist):
		if bedpe.o1 == "+":
			print bedpe.c1 + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e1+500) + "\t" + bedpe.name + "," + bedpe.score + ":intra:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"+" + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e1+500) + "\t" + color + "\t" + "2" + "\t" + \
				str(bedpe.e1 - bedpe.s1) + "," +  "1" + "\t" + \
				"0," +	str((bedpe.e1-bedpe.s1)+499)

		if bedpe.o1 == "-":
			print bedpe.c1 + "\t" + str(bedpe.s1-500) + "\t" + str(bedpe.e1) + "\t" + bedpe.name + "," + bedpe.score + ":intra:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"-" + "\t" + str(bedpe.s1-500) + "\t" + str(bedpe.e1) + "\t" + color + "\t" + "2" + "\t" + \
				"1" + "," + str(bedpe.e1 - bedpe.s1) + "\t" + \
				"0," + str(500)
	
		if bedpe.o2 == "+":
			print bedpe.c2 + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + bedpe.name + "," + bedpe.score + ":intra:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"+" + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + color + "\t" + "2" + "\t" + \
				str(bedpe.e2 - bedpe.s2) + "," +  "1" + "\t" + \
				"0," +	str((bedpe.e2-bedpe.s2)+499)
		
		if bedpe.o2 == "-":
			print bedpe.c2 + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + bedpe.name + "," + bedpe.score + ":intra:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e2) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"-" + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + color + "\t" + "2" + "\t" + \
				"1" + "," + str(bedpe.e2 - bedpe.s2) + "\t" + \
				"0," + str(500)
		
	# interchromosomals:	
	elif (bedpe.c1 != bedpe.c2):
		if bedpe.o1 == "+":
			print bedpe.c1 + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e1+500) + "\t" + bedpe.name + "," + bedpe.score + ":inter:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"+" + "\t" + str(bedpe.s1) + "\t" + str(bedpe.e1+500) + "\t" + color + "\t" + "2" + "\t" + \
				str(bedpe.e1 - bedpe.s1) + "," +  "1" + "\t" + \
				"0," +	str((bedpe.e1-bedpe.s1)+499)

		if bedpe.o1 == "-":
			print bedpe.c1 + "\t" + str(bedpe.s1-500) + "\t" + str(bedpe.e1) + "\t" + bedpe.name + "," + bedpe.score + ":inter:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"-" + "\t" + str(bedpe.s1-500) + "\t" + str(bedpe.e1) + "\t" + color + "\t" + "2" + "\t" + \
				"1" + "," + str(bedpe.e1 - bedpe.s1) + "\t" + \
				"0," + str(500)
	
		if bedpe.o2 == "+":
			print bedpe.c2 + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + bedpe.name + "," + bedpe.score + ":inter:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e1) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"+" + "\t" + str(bedpe.s2) + "\t" + str(bedpe.e2+500) + "\t" + color + "\t" + "2" + "\t" + \
				str(bedpe.e2 - bedpe.s2) + "," +  "1" + "\t" + \
				"0," +	str((bedpe.e2-bedpe.s2)+499)
		
		if bedpe.o2 == "-":
			print bedpe.c2 + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + bedpe.name + "," + bedpe.score + ":inter:" + bedpe.c1 + ":" + str(bedpe.s1) + "-" + str(bedpe.e2) + "," + \
				bedpe.c2 + ":" + str(bedpe.s2) + "-" + str(bedpe.e2) + "\t" + str(abs(bedpe.e2-bedpe.s1)) + "\t" + \
				"-" + "\t" + str(bedpe.s2-500) + "\t" + str(bedpe.e2) + "\t" + color + "\t" + "2" + "\t" + \
				"1" + "," + str(bedpe.e2 - bedpe.s2) + "\t" + \
				"0," + str(500)

def processBEDPE(bedpeFile, name, dist):
	"""
	Process the BEDPE file and convert each entry to SAM.
	"""
	writeTrackName(name)
	if bedpeFile == "stdin":		
		for line in sys.stdin:
			lineList = line.strip().split()
			if (len(lineList) > 0):
				bedpe = BEDPE(lineList)
				bedpeToBlockedBed(bedpe, dist)
	else:
		for line in open(bedpeFile, 'r'):
			lineList = line.strip().split()
			if (len(lineList) > 0):
				bedpe = BEDPE(lineList)
				bedpeToBlockedBed(bedpe, dist)


def writeTrackName(name):
	print "track name=" + name + " itemRgb=On"


def main():
	usage = """%prog -i <file> -n <name> -d <dist>

bedpeToBed12 version 1.0
Author: Aaron Quinlan & Ira Hall	
Description: converts BEDPE to BED12 format for viewing in IGV or the UCSC browser.
Last Modified: July 20, 2010 

	"""
	parser = OptionParser(usage)

	parser.add_option("-i", "--bedpe", dest="bedpe",
		help="BEDPE input file", metavar="FILE")

	parser.add_option("-n", "--name", default="BEDPE", dest="name", type="str",
		help="The name of the track.  Default is 'BEDPE'.",
		metavar="STR")

	parser.add_option("-d", "--maxdist", dest="dist", default = 1000000, type="int",
		help="The minimum distance for drawing intrachromosomal features as if they are interchromosomal (i.e., without a line spanning the two footprints). Default is 1Mb.",
		metavar="INT")

	(opts, args) = parser.parse_args()

	if opts.bedpe is None:
		parser.print_help()
		print
	else:
		processBEDPE(opts.bedpe, opts.name, opts.dist)

if __name__ == "__main__":
	main()



