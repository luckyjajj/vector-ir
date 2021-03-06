import sys
import os
import getopt
import pickle
import porterAlgo


class FileParser:
	def __init__(self, path, commonWords, stopWord):
		self.path = path
		self.temp = []
		self.grandList = []
		self.cWords = []
		self.titleList = []
		self.commonFlag = commonWords
		self.stopFlag = stopWord
		self.titleAbstract = []
		self.author = []

	def parseFile(self):
		p = porterAlgo.PorterStemmer()
		#Reads file line by line and compares with cWords list, inserting valid terms into grandList
		file = open(self.path, 'r')
		for line in file:
			self.count = 0
			for word in line.split():

				#For .I (Index Number)
				if word == '.I':
					for word in line.split():
						if word != '.I':
							indexNum = int(float(word))

				#For .T (Title)
				if word == '.T':
					self.titleTemp = ''
					for line in file:
						for word in line.split():
							self.count += 1
							if word == '.B' or word == '.W':
								break
							goodWord = ''
							self.titleTemp += word + ' '
							for j in self.titleAbstract:
								if j[0] == indexNum:
									j[1].append(word)
									break
							else:
								self.titleAbstract.append([indexNum, [word]])
							for c in word:
								if c.isalnum() or c == '-' or c == '+' or c == '*' or c == '/':
									goodWord += c.lower()
							if self.stopFlag == True:
								goodWord = p.stem(goodWord, 0, len(goodWord)-1)
							for x in self.cWords: 
								intoArray = ''
								if goodWord == x:
									break
							else:
								for y in self.grandList:
									if y[0] == goodWord:
										y[1].append((indexNum, self.count))
										break
								else:
									temp = [goodWord, [(indexNum, self.count)]]
									self.grandList.append(temp)
						if word == '.B' or word == '.W':
							self.titleList.append((indexNum, self.titleTemp.strip()))
							break

				#For .W (Abstract)
				if word == '.W':
					self.count -=1
					for line in file:
						if word == '.B':
							break
						for word in line.split():
							self.count += 1
							if word == '.B':
								break
							goodWord = ''
							for j in self.titleAbstract:
								if j[0] == indexNum:
									j[1].append(word)
									break
							for c in word:
								if c.isalnum() or c == '-' or c == '+' or c == '*' or c == '/':
									goodWord += c.lower()
							if self.stopFlag == True:
								goodWord = p.stem(goodWord, 0, len(goodWord)-1)
							for x in self.cWords:
								if goodWord == x:
									break
							else:
								for y in self.grandList:
									if y[0] == goodWord:
										y[1].append((indexNum, self.count))
										break
								else:
									temp = [goodWord, [(indexNum, self.count)]]
									self.grandList.append(temp)
													
				
				#For .T (Title)
				if word == '.A':
					self.authorTemp = ''
					for line in file:
						for word in line.split():
							if word == '.N' or word == '.K' or word == '.C':
								break
							self.authorTemp += word + ' '

						if word == '.N' or word == '.K' or word == '.C':
							self.author.append((indexNum, self.authorTemp.strip()))
							break	


	def commonWords(self):
		#Read common word file and load it into a array
		file = open('CACM/common_words', 'r')
		if self.commonFlag == True:
			for line in file:
				for word in line.split():
					self.cWords.append(word)

	def getGrandList(self):
		return self.grandList
	def getTitleList(self):
		return self.titleList
	def getTitleAbstract(self):
		return self.titleAbstract
	def getAuthorAbstract(self):
		#print self.author
		return self.author

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
	
	def __init__(self, tlist):
		self.terms = tlist
		self.index = None
		self.termfile = []
		self.postfile =[]

	def buildTree(self):
		self.index = Tree()
		for term in self.terms:
			self.index.add(term[0],term[1])

	def compileIndexTerms(self, subtree=None):
		if subtree == None:
			subtree = self.index.tree

		for node in subtree:
			if not node.link:
				data = [node.getWord(),node.getPostLength()]
				self.termfile.append(data)
			else:
				self.compileIndexTerms(node.link)

	def compileIndexPostLink(self, subtree=None):
		if subtree == None:
			subtree = self.index.tree

		for node in subtree:
			if not node.link:
				data = [node.getPostLink()]
				self.postfile.append(data)
			else:
				self.compileIndexPostLink(node.link)

	def saveTermfile(self):
		self.compileIndexTerms()
		with open('dictionary.pk', 'wb') as output:
			pickle.dump(self.termfile, output, pickle.HIGHEST_PROTOCOL)


	def savePostfile(self):
		self.compileIndexPostLink()
		with open('postfile.pk', 'wb') as output:
			pickle.dump(self.postfile, output, pickle.HIGHEST_PROTOCOL)

	def saveTitleFile(self,data):
		with open('titleList.pk', 'wb') as output:
			pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
			
	def saveAbstractFile(self,data):
		with open('titleAbstract.pk', 'wb') as output:
			pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)	
			
	def saveAuthorTemp(self,data):
		with open('author.pk', 'wb') as output:
			pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)


def main(argv):
	inputfile = ''
	commonWords = True
	stopWords = True
	
	try:
		opts, args = getopt.getopt(argv, "hi:cs",["ifile="])
	except getopt.GetoptError:
		print 'invert.py -i <inputfile>'
		sys.exit(2)
	
	if not opts:
		print 'invert.py -i <inputfile>'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'invert.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt == '-c':
			commonWords = False
		elif opt == '-s':
			stopWords = False
			
	
	x = FileParser(inputfile, commonWords, stopWords)
	x.commonWords()
	x.parseFile()

	index = Index(x.getGrandList())
	index.buildTree()
	index.saveTermfile()
	index.savePostfile()
	index.saveTitleFile(x.getTitleList())
	index.saveAbstractFile(x.getTitleAbstract())
	index.saveAuthorTemp(x.getAuthorAbstract())

if __name__ == '__main__':
	main(sys.argv[1:])
