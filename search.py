import Tkinter
import tkMessageBox
import sys
import os
import getopt
import pickle
import porterAlgo
import time
import math

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
		self.termFreq = [];

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

		return self.documents.__len__()
	
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
		
	def printData(self,post,node):
		for document in self.documents:
			for title in self.titleList:
				if (document == title[0]):
					print title[0],'   ',title[1]
					print 'Found ' + str(self.termFreq(title[0],post)) + ' term(s) in this document.'
					node.termFreq.append((title[0],self.termFreq(title[0],post)));
					print 'The position is/are ' + str(self.displayPosition(title[0],post)) + '.'
					print self.context(title[0], post)
		self.documents = []
					
	def clear (self):
		self.documents = []

	def search(self, term):
		node=0
		if (self.stemFlag):
			p = porterAlgo.PorterStemmer()
			term = p.stem(term.lower(),0, term.__len__()-1)
		node = self.index.search(term) 
		if (node != 0):
			post = node.getPostLink()
			#print self.documentFreq(post)
			#self.printData(post,node)

			return node
		else: 
			return node

class docObject:
	def __init__(self, idz, iterms):
		self.docID = idz
		self.terms = []
		for term in iterms:
			self.terms.append([term,0])
		self.wtf = []
		self.w = []
		self.cosine = 0 
		self.docVector = 0
	
	def addTerm(self, term):
		self.terms.append(term)

	def doSim(self, qw, qv):
		total = 0;
		i = 0;
		for weight in self.w:
			temp = weight*qw[0]
			total = total + temp
			i = i +1

		#print total
		#print (self.docVector * qv)
		self.cosine = total / (self.docVector * qv)
		#print total	



	def plusOne(self, term):
		for termz in self.terms:
			if termz[0] == term:
				termz[1] = termz[1] + 1

	def doWTF(self):
		for term in self.terms:
			if (term[1] == 0):
				self.wtf.append(0)
			else:
				self.wtf.append(1 + math.log10(term[1]))
			#print math.log10(term[1])
			#self.wtf.append(1 + math.log10(term[1]))
	def doWeight(self,idf):
		i = 0
		for term in self.terms:
			#print idf * wtf[i]
			#print idf[i]
			self.w.append(idf[i]*self.wtf[i])
			i = i +1
	def doDocVector(self):
		total = 0;
		for weight in self.w:
			j = weight * weight
			total = total+ j
		self.docVector = math.sqrt(total)


class docHandler:
	def __init__(self, freq):
		self.masterTable = []
		self.qtf = freq
		self.qw = []
		self.qv = 0
		self.finalList = []

	def doQueryWeight(self):
		for tf in self.qtf:
			if (tf == 0):
				self.qw.append(0)
			else:
				self.qw.append(1 + math.log10(tf))
	def doQueryVector(self):
		total =0
		for weight in self.qw:
			j = weight * weight
			total = total+ j
		self.qv = math.sqrt(total)

	def addDoc(self, postLink, terms ,term):
		for link in postLink:
			#print link[0] 
			if self.containDoc(link[0]) == False:
				table = docObject(link[0],terms)
				table.plusOne(term)
				self.masterTable.append(table)
			else:
				table = self.getTable(link[0])
				table.plusOne(term)

	def containDoc(self, idz):
		if self.masterTable.__len__() == 0:
			return False
		else:
			for table in self.masterTable:
				if (table.docID == idz):
					return True
			return False 

	def getTable(self, idz):
		for table in self.masterTable:
			if (table.docID == idz):
				return table

	def calcWTF(self):
		for table in self.masterTable:
			table.doWTF()

	def calcWeight(self, idf):
		for table in self.masterTable:
			table.doWeight(idf)

	def calcDVector(self):
		for table in self.masterTable:
			table.doDocVector()

	def calcSim(self):
		for table in self.masterTable:
			table.doSim(self.qw, self.qv)

	def sortFinal(self):
		for table in self.masterTable:
			#print table.cosine
			temp = [table.cosine, table.docID]
			self.finalList.append(temp)

		self.finalList.sort(reverse=True);




def main(argv):
	##app = gUI(None)
	#app.title('Query Search')
	#app.mainloop()
	query = [['monica',1],['california',1]]
	queryz = []
	freq =[]
	for i in query:
		freq.append(i[1])
		queryz.append(i[0])

	index = Index(False)
	index.loadData()
	results = []
	df = []
	idf = []
	mT = docHandler(freq)

	for term in query:
		result = index.search(term[0])
		results.append(result)
		df.append(index.documentFreq(result.getPostLink()))
		idfR = math.log10(3204.00/index.documentFreq(result.getPostLink()))
		idf.append(idfR)
		mT.addDoc(result.getPostLink(), queryz, term[0])
		index.clear()

	mT.calcWTF()
	mT.calcWeight(idf)
	mT.calcDVector()
	mT.doQueryWeight()
	mT.doQueryVector()
	mT.calcSim()
	mT.sortFinal()

	test = mT.getTable(1164)
	#test = mT.getTable(3036)

	
	
	print mT.finalList


class gUI(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		self.stem = False
		self.common = False
		result = tkMessageBox.askquestion("Query Search", "Stemmed?")
		if result == 'yes':
			self.stem = True
		result = tkMessageBox.askquestion("Query Search", "With Common Words?")	
		if result == 'yes':
			self.common = True
		# if (self.stem == False and self.common == False):
			# os.system("py invert.py -i CACM/cacm.all -s")
		# elif (self.stem == True and self.common == True):
			# os.system("py invert.py -i CACM/cacm.all -c")		
		# elif (self.stem == False and self.common == True):
			# os.system("py invert.py -i CACM/cacm.all -sc")		
		# else:
			# os.system("py invert.py -i CACM/cacm.all")			
		
		self.grid()
		self.entryVariable = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')
		self.entryVariable.set("Enter query here.")
		
		button = Tkinter.Button(self,text="Search!", command=self.OnButtonClick)
		button.grid(column=1,row=0)
		
		self.labelVariable = Tkinter.StringVar()
		label = Tkinter.Label(self,textvariable=self.labelVariable, anchor="w")
		label.grid(column=0,row=1,columnspan=2,sticky='EW')
		self.labelVariable.set("RESULT!!!!!")	
		
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		self.geometry("800x800")
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
	
	def OnButtonClick(self):
		self.queryArray = []
		temp = ""
		for char in self.entryVariable.get():
			if char.isalnum():
				temp += char.lower()
				print temp
			else:
				self.queryArray.append(temp)
				temp = ""
		if temp != "":
			self.queryArray.append(temp)
		print self.queryArray
		self.labelVariable.set( self.entryVariable.get())   ##### this has to be changed so that it sets result as the label variable  #####
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)




if __name__ == '__main__':
	main(sys.argv[1:])
