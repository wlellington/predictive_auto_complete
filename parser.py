# Wesley Ellington
# CSE 3353 

# Text parser for creating trie from large text documents
# and gathering timing data on average access times

import glob
import pickle
import trie
import os.path
import string
import time
import itertools

def timeSearches(completions, maxlen):

	output = open("timing.txt", "w")
	prev = ''

	# iterate over prefix sizes
	for i in range(1, maxlen + 1):
		times = []
		total = 0
		print "Running timings on length " + str(i)

		# for every possible string of length i
		for query in itertools.imap(''.join, itertools.product(string.ascii_lowercase, repeat=i)):
		    	# run test on each string
			stime = time.clock()
			completions.getRecs(prev, query)
			etime = time.clock()

			# add times taken to list
			times.append(etime - stime)
			prev = query
		
		# sum times
		for sample in times:
			total += sample

		# average to size of data set
		total = (total / len(times)) * 1000

		# print to file
		output.write("( " + str(i) + ", "+ str(total) + " )\n")

	output.close()

	print "Done!"

if __name__ == "__main__":
	
	words = []
	linewords = []
	completions =  trie.Trie()
	
	# check if pickle exsists
	if os.path.isfile("completions.pkl"):
		print "Pickle already exists!\n Importing from file..."

		# open pickle file
		inpickle = open("completions.pkl", "rb")

		# load stucture from file
		completions = pickle.load(inpickle)

		# close pickle
		inpickle.close()

	else:	
		# create list of filenames for processing
		files = glob.glob("./inputtext/*.txt")
		previous = ''
		new = ''
		for text in files:
			print "Parsing " + text

			# open text file
			infile = open(text, "r")
			
			# iterate over lines
			for line in infile:
				# split line into words
				linewords = line.split()

				# add words to master list
				for word in linewords:
					# cast to lower case
					word = word.lower()
					# clean punctuation
					word = word.translate(None, string.punctuation)
					words.append(word)

			# reverse list to maintain order of previous word lookup
			words = words[::-1]
			
			# add words to trie structure
			while len(words) > 1:
				# add word to trie, remove from list
				new = words.pop()
				# if no previous word exists
				if previous == "":
					# include no history info
					completions.insert(new)

				# create new insertion with history
				else:
					completions.insertHist(previous, new)
				
				# update previous for next iteration
				previous = new

			# close text file
			infile.close()	

		# open output file for pickler
		outfile = open("completions.pkl", "wb")

		# output trie to pickle
		pickle.dump(completions, outfile)

		# close pkl file
		outfile.close()

	timeSearches(completions, 5)
