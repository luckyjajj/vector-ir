import sys
import os
import getopt
import pickle
import porterAlgo

class FileParser:
	def __init__(self, commonWords, stopWord):
		self.temp = []
		self.grandQuery = []
		self.cWords = []
		self.titleList = []
		self.commonFlag = commonWords
		self.stopFlag = stopWord
		self.titleAbstract = []

	def parseFile(self):
		p = porterAlgo.PorterStemmer()
		#Reads file line by line and compares with cWords list, inserting valid terms into grandQuery
		file = open("CACM/query.text", 'r')
		for line in file:
			self.count = 0
			for word in line.split():

				#For .I (Index Number)
				if word == '.I':
					for word in line.split():
						if word != '.I':
							indexNum = int(float(word))

				#For .W (Query)
				if word == '.W':
					self.count = 1
					for line in file:
						if word == '.N' or word == '.A':
							break
						for word in line.split():
							if word == '.N' or word == '.A':
								break
							goodWord = ''
							# for j in self.titleAbstract:
								# if j[0] == indexNum:
									# j[1].append(word)
									# break
							for c in word:
								if c.isalnum(): #or c == '-' or c == '+' or c == '*' or c == '/':
									goodWord += c.lower()
							# if self.stopFlag == True:
								# goodWord = p.stem(goodWord, 0, len(goodWord)-1)
							# for x in self.cWords:
								# if goodWord == x:
									# break
							for y in self.grandQuery:
								if y[0] == indexNum:
									for z in y[1]:
										if z[0] == goodWord:
											z[1] += 1
											break
									else:
										y[1].append([goodWord, self.count])
									break
							else:
								temp = [indexNum, [[goodWord, self.count]]]
								self.grandQuery.append([indexNum, [[goodWord, self.count]]])
			
		print self.grandQuery

	# def commonWords(self):
		# #Read common word file and load it into a array
		# file = open('CACM/common_words', 'r')
		# if self.commonFlag == True:
			# for line in file:
				# for word in line.split():
					# self.cWords.append(word)

	#def getGrandQuery(self):

	# def getTitleList(self):
		# return self.titleList
	# def getTitleAbstract(self):
		# return self.titleAbstract
		
def main(argv):
	commonWords = True
	stopWords = True
	
	x = FileParser(commonWords, stopWords)
	#x.commonWords()
	x.parseFile()
	

if __name__ == '__main__':
	main(sys.argv[1:])