import sys
import os
import getopt
import pickle

class Node:
	"""
		Node for Tree data structure
	"""
	def __init__(self, word, level, postLink):
		self.link = []
		if (level < word.__len__()):
			self.char = word[level]
		else:
			self.char = ' '
		self.word = word
		self.postLink = postLink

	def changeChar(self,level):
		if (level < self.word.__len__()):
			self.char = self.word[level]
		else:
			self.char = ' '

	def clearWord(self):
		self.word = None

	def clearPostLink(self):
		self.postLink = []

	def getPostLength(self):
		return len(self.postLink)

	def getPostLink(self):
		return self.postLink

	def getWord(self):
		return self.word
	
	def getChar (self):
		return self.char


class Tree:
	"""
		Search tree data structure for document index
	"""
	def __init__(self):
		self.tree = []

	def add(self, word=None, postLink=[],level=0,subtree=None):
		connection = False
		x = Node(word,level,postLink)
		x.changeChar(level)
		newSubTree = None
		if (level == 0):
			subtree = self.tree

		for node in subtree:
			if (x.getChar() == node.getChar()):
				connection = True
				newSubTree = node.link
				if (node.getWord() != None):
					self.add(node.getWord(),node.getPostLink(),level+1,newSubTree)
				node.clearWord()
				node.clearPostLink()
				break

		if (connection):
			del x
			self.add(word,postLink,level+1,newSubTree)
			pass
		else:
			subtree.append(x)			

	def search(self, word, subtree=None, oword=None):
		if (oword == None):
			oword = word
		if (subtree == None):
			subtree = self.tree

		for node in subtree:
			if (node.getWord() == oword):
				return 'found'
			elif (node.getChar() == word[0]):
				#print word
				return self.search(word[1:],node.link,oword)
		else:
			return 'not found'


	
	def showTree(self,subtree=None):
		for node in subtree:
			if not node.link:
				print node.getWord(),
				print node.getPostLink()
			else:
				if (node.getWord()!= None):
					print node.getWord(),
					print node.getPostLink()
				print node.getChar()
				self.showTree(node.link)

class Index:
	def __init__(self):
		self.index = None
		self.termfile = None
		self.postfile =None

	def loadData(self):
		file1 = open("dictionary.pk",'r')
		self.termfile = pickle.load(file1)
		file2 = open("postfile.pk",'r')
		self.postfile = pickle.load(file2)
		self.buidTree()

	def buidTree(self):
		self.index = Tree()
		i =0
		for term in self.termfile:
			self.index.add(term[0],self.postfile[i])
			i = i +1


def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv, "h:",["ifile="])
	except getopt.GetoptError:
		print 'test.py'
		sys.exit(2)
			
	for opt, arg in opts:
	
		if opt == '-h':
			print 'test.py'
			sys.exit()

	index = Index()
	index.loadData()
	
	print 'ZZEND to quit'
	while True:
		term = raw_input("Enter search term: ")
		if (term != 'ZZEND'):
			print index.index.search(term)
		else:
			sys.exit()
		pass

if __name__ == '__main__':
	main(sys.argv[1:])


