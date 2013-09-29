import sys
import os
import getopt
import porterAlgo

class FileParser:
	def __init__(self, path):
		self.path = path
		self.temp = []
		self.grandList = []
		self.cWords = []
		self.stemWord = ''

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
					for line in file:
						for word in line.split():
							self.count += 1
							if word == '.B' or word == '.W':
								break
							goodWord = ''
							for c in word:
								if c.isalnum() or c == '-' or c == '+' or c == '*' or c == '/':
									goodWord += c.lower()
							stemWord = p.stem(goodWord, 0, len(goodWord)-1)
							for x in self.cWords: 
								intoArray = ''
								if stemWord == x:
									break
							else:
								for y in self.grandList:
									if y[0] == stemWord:
										y[1].append((indexNum, self.count))
										break
								else:
									temp = [stemWord, [(indexNum, self.count)]]
									self.grandList.append(temp)
						if word == '.B' or word == '.W':
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
							for c in word:
								if c.isalnum() or c == '-' or c == '+' or c == '*' or c == '/':
									goodWord += c.lower()
							stemWord = p.stem(goodWord, 0, len(goodWord)-1)
							for x in self.cWords:
								if stemWord == x:
									break
							else:
								for y in self.grandList:
									if y[0] == stemWord:
										y[1].append((indexNum, self.count))
										break
								else:
									temp = [stemWord, [(indexNum, self.count)]]
									self.grandList.append(temp)
		print(self.grandList)

	def commonWords(self):
		#Read common word file and load it into a array
		file = open('CACM/common_words', 'r')
		for line in file:
			for word in line.split():
				self.cWords.append(word)
	
# class Tree:
# 	#Indexer data structure
# 	def __init__(self):
# 		pass

# class Node:
# 	#Elements in a tree
# 	def __init__(self):
# 		pass

# class Indexer:
# 	def __init__(self):
# 		self.terms = [['google', [(1,1),(1,50)]],['cat',[(2,3)]]] #practic terms
# 		pass
# 	def buildTree(self):
# 		#Build tree
# 		print self.terms[0][1][1]
# 		pass

def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:",["ifile="])
	except getopt.GetoptError:
		print('vectorir.py -i <inputfile>')
		sys.exit(2)
	
	if not opts:
		print ('vectorir.py -i <inputfile>')
		sys.exit(2)
	
	for opt, arg in opts:
		#print opts
		if opt == '-h':
			print('vectorir.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	#test = Indexer()
	#test.buildTree()
	x = FileParser(inputfile)
	x.commonWords()
	x.parseFile()

    #print('Hello')
if __name__ == '__main__':
    main(sys.argv[1:])