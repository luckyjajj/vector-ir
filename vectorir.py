import sys
import os
import getopt

class FileParser:
	def __init__(self, path):
		self.path = path
		self.wordList = []
		self.cWords = []
		self.flag = 0
	def parseFile(self):
		#Reads file line by line and calls other methods for each line event
		file = open(self.path, 'r')
		for line in file:
			for word in line.split():
				if word == '.I':
					pass
				if word == '.T':
					pass
				if word == '.W':
					pass			
		pass
	def commonWords(self):
		#Read common word file and load it into a array
		file = open('CACM/common_words', 'r')
		for line in file:
			for word in line.split():
				self.cWords.append(word)
		pass
	
class Tree:
	#Indexer data structure
	def __init__(self):
		self.tree = []
		pass
	def add(self, word=None, postLink=[]):
		x = Node(word,postLink)
		#x.displayWord()
		self.tree.append(x)
		pass
	def search(self, word):
		pass
	def showTree(self):
		print self.tree

class Node:
	#Elements in a tree
	def __init__(self, word, postLink):
		self.link = []
		self.word = word
		self.postLink = postLink
		pass
	def displayWord(self):
		print self.word


class Indexer:
	def __init__(self):
		self.terms = [['google', [(1,1),(1,50)]],['cat',[(2,3)]]] #practic terms
		pass
	def buildTree(self):
		#Build tree
		print self.terms[0][1][1]
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
	test = Tree()
	test.add('google')
	#test.showTree()
	#test.tree[0].displayWord()



if __name__ == '__main__':
    main(sys.argv[1:])