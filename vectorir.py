import sys
import os
import getopt

class FileParser:
	def __init__(self, path):
		self.path = path
	def parseFile(self):
		#Reads file line by line and calls other methods for each line event
		pass
	def commonWords(self):
		#Read common word file and load it into a array
		pass
	

class Indexer:
	def __init__(self):
		pass
	def buildTree(self):
		#Build tree
		pass


def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:",["ifile="])
	except getopt.GetoptError:
		print 'vectorir.py -i <inputfile>'
		sys.exit(2)
	
	if not opts:
		print 'vectorir.py -i <inputfile>'
		sys.exit(2)
	
	for opt, arg in opts:
		#print opts
		if opt == '-h':
			print 'vectorir.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg

    #print('Hello')
if __name__ == '__main__':
    main(sys.argv[1:])