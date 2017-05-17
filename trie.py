# Wesley Ellington
# CSE 3353

# Trie class for autocomplete algorithm
# defaultdict() implmentation idea expanded 
# http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python


from collections import defaultdict
import operator

class Trie:
	

	# initialization
	def __init__(self):
		self.root = defaultdict()
		self.history = defaultdict()
		self.totalsize = 0
		self.numwords = 0

	# insert new word with history information
	def insertHist(self, prev, curr):
		# update size
		self.totalsize += 1
		# add word to trie, save frequency
		thisFreq = self.insert(curr)
		current = self.history
		# freq of one implies new word, update counter if so
		if thisFreq == 1:
			self.numwords += 1

		# add history info if word is above commonality threshhold
		if thisFreq > 5:
			current = current.setdefault(prev, {})
			current.setdefault(curr, 30)
			current[curr] += 30 * (thisFreq ** float(1/2))

	# add word to trie
	def insert(self, word):
		#starting at root
		current = self.root
		#looping over word
		for letter in word:
			#set default value for internal letter
			#then set current location to interal
			current = current.setdefault(letter, {})
		# after assinging all letters, set end value
		current.setdefault("_end")
		# if adding new word, initialize value to 0
		if(current["_end"] == None):
			current["_end"] = 0
		# incrament freq count by one
		current["_end"]  += 1

		return current["_end"]

	# see if word exists exactly
	def search(self, word):
		# starting at root
		current = self.root
		# loop over word
		for letter in word:
			# if the letter is not in current loc, return false
			if letter not in current:
				return False
			# move into trie
			current  = current[letter]
		# if found value contains end conidition, return true
		if "_end" in current:
			return True
		return False

	# check for existance of words staring with prefix
	def startsWith(self, prefix):
		# starting at root
		current = self.root

		# check inward in trie
		for letter in prefix:
			# if prefix goes into uncreated space, return false
			if letter not in current:
				return False
			# update current
			current = current[letter]
		return True

	# get list completion strings
	def getComps(self, prefix):
		# starting at root
		current = self.root
		results = []
	
		# check inward to get to end of prefix
		for letter in prefix:
			# navigate to end of prefix, else return ''
			if letter not in current:
				return ''
			current = current[letter]
		# starting at end of prefix
		endings = self.depthFirst(current)

		# attach prefix to make whole word
		for term in endings:
			term[0] = prefix + term[0]
			results.append(term)

		return results


	# get list of recommended completions
	def getRecs(self, previous, prefix):
		results = [["", 0]]

		# get list of completions
		results =  self.getComps(prefix)

		# check if previous word shows up in history
		if previous in self.history:

			# Open dict of history values
			current = self.history[previous]

			# search all suggestions
			for suggestion in results:
				if suggestion[0] in current:
					# scale score of suggestion by history weight
					suggestion[1] = suggestion[1] * current[suggestion[0]]

		# sort list for top recommendations
		if type(results) is list:
			results.sort(key=lambda x: x[1])

		# cut down list to ten
		if len(results) >= 10:
			return results[-1:-10:-1]
		else:
			return results[::-1]

	# gets top three suggestions, strips 
	def shortRecs(self, previous, prefix):
		results = self.getRecs(previous, prefix)
		if len(results) > 3:
			results = results[0:3]

		short = []
		for value in results:
			short.append(value[0])

		return short
		
	def depthFirst(self, root):
		current = root
		results = []
		
		for key in current:
			endterm = []
			group = []

			if key != "_end":
				group = self.depthFirst(current[key])
			
			# if there is an end node
			if key == "_end":
				endterm = ["", current["_end"]]
				group.append(endterm)
			
			# add key to make string better
			for value in group:
				if key != "_end":
					value[0] = key + value[0]	
				results.append(value)
		
		return results


if __name__ == "__main__":
	test = Trie()
	test.insert("memes")
	test.insert("memes")
	test.insert("maymays")
	test.insert("meemees")
	test.insert("semem")
	test.insert("meimei")
	test.insert("moimoi")

	print test.search("memes")
	print test.search("higgs")
	print test.startsWith("me")
	print test.root
	print test.getRecs("m")
	print test.getRecs("")
