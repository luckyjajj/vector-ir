import sys
import os
import getopt
import pickle
import porterAlgo
import time

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
		try:
			temp = word[0]
		except IndexError:
			temp = ' '

		for node in subtree:
			if (node.getWord() == oword):
				return node
			elif (node.getChar() == temp):
				return self.search(word[1:],node.link,oword)
		else:
			return 0


	
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
	def __init__(self, stemFlag):
		self.index = None
		self.termfile = None
		self.postfile =None
		self.titleAbstract = None
		self.titleList = None
		self.titleAbstract = None
		self.stemFlag = stemFlag
		self.documents = []


	def loadData(self):
		file1 = open("dictionary.pk",'rb')
		self.termfile = pickle.load(file1)
		file2 = open("postfile.pk",'rb')
		self.postfile = pickle.load(file2)
		self.buidTree()
		file3 = open("titleList.pk", "rb")
		self.titleList = pickle.load(file3)
		file4 = open("titleAbstract.pk", "rb")
		self.titleAbstract = pickle.load(file4)

	def buidTree(self):
		self.index = Tree()
		i =0
		for term in self.termfile:
			self.index.add(term[0],self.postfile[i][0])
			i = i +1
			
	def documentFreq(self, post):
		for occurence in post:
			if (occurence[0] in self.documents):
				pass
			else:
				self.documents.append(occurence[0])

		return 'We found '+str(self.documents.__len__())+' documents\n'
	
	def termFreq(self,idz,post):
		total = 0
		for occurence in post:
			if (idz == occurence[0]):
				total = total +1
		return total
		
	def displayPosition(self,idz, post):
		pos = []
		for occurence in post:
			if (idz == occurence[0]):
				pos.append(occurence[1])
		return pos
		
	def context(self, idz, post):
		temp = ''
		start = 0
		end = 0
		self.pos=0
		for occurence in post:
			if (idz == occurence[0]):
				self.pos = occurence[1]
				break
		for subList in self.titleAbstract:
			if (idz == subList[0]):
				if self.pos - 6 <= 0:
					start = 0
				else:
					start = self.pos - 6
				if self.pos + 5 >= len(subList[1]):
					end = len(subList[1])
				else:
					end = self.pos + 5
				for k in subList[1][start:end]:
					temp += k + ' '
		return(temp + '\n\n')
		
	def printData(self,post):
		for document in self.documents:
			for title in self.titleList:
				if (document == title[0]):
					print title[0],'   ',title[1]
					print 'Found ' + str(self.termFreq(title[0],post)) + ' term(s) in this document.'
					print 'The position is/are ' + str(self.displayPosition(title[0],post)) + '.'
					print self.context(title[0], post)
					
	def search(self, term):
		node=0
		if (self.stemFlag):
			p = porterAlgo.PorterStemmer()
			term = p.stem(term.lower(),0, term.__len__()-1)
			node = self.index.search(term) 
		if (node != 0):
			post = node.getPostLink()
			print self.documentFreq(post)
			self.printData(post)

			return 'Found'
		else: 
			return 'Not Found'

def main(argv):
	inputfile = ''
	stemFlag = True
	try:
		opts, args = getopt.getopt(argv, "hs")
	except getopt.GetoptError:
		print 'test.py -h Help -s Disable stemming'
		sys.exit(2)
			
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py:'
			sys.exit()
		elif opt  == '-s':
			stemFlag = False


	index = Index(stemFlag)
	index.loadData()
	times = []
	print 'ZZEND to quit'
	while True:
		
		term = raw_input("Enter search term: ")
		if (term != 'ZZEND'):
			t0 = time.time()
			print index.search(term)
			t1 = time.time()
			timez = t1-t0
			print 'Time of search:', timez
			times.append(timez)
		else:
			i = 0
			total = 0
			for timez in times:
				total = total + timez
				i = i +1

			print 'Average time for all searches: ',total/i

			sys.exit()
		pass

if __name__ == '__main__':
	main(sys.argv[1:])


