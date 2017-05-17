

# Wesley Ellington
# CSE 3353

import trie
import parser
import pickle
import curses.ascii
import sys
import tty

class Interface:
	completions = trie.Trie()
	userbuffer = ''
	suggestions = []

	# initialize trie
	def __init__(self, filename):

		# load pickle config
		print "Initializing..."
		infile = open(filename, "rb")
		self.completions = pickle.load(infile)
		infile.close()

		self.userbuffer = []
		self.userview = ''
		self.suggestions = []
		print "Completion data loaded"

	# enter loop structure
	def start(self):
		print "Hooking on to terminal..."
		self.userloop()

	# master control loop, handles user input
	def userloop(self):
		kill = False
		wordbuffer = ''
		recs = []
		while kill == False:
			key = getch()
			#print repr(key)

			# add word to word list
			if key == ' ':
				prev = ''
				if len(self.userbuffer) != 0 :
					prev = self.userbuffer[-1]
				self.userbuffer.append(wordbuffer)
				self.completions.insertHist(prev, wordbuffer)
				wordbuffer = ''
			
			# move back one char if del
			elif key == '\x7f':
				# if whole word is deleted, add prev from list
				if len(wordbuffer) != 0:
					# shorten word
					wordbuffer = wordbuffer[0:-1]
				else:
					# add previous word for edit
					if(len(self.userbuffer) != 0):
						wordbuffer = self.userbuffer.pop()

			# kill if ctl c
			elif key == '\x03':
				kill = True
	
			# end program on ctl q
			elif key == '\x11':
				self.stop()

			# dump line on enter
			elif key == '\r':
				print '\n\n'
				# pass to shell
				wordbuffer = ''
				self.userbuffer = []
			
			# if tab, replace current word with top suggestion
			elif key == '\t':
				if len(recs) != 0:
					wordbuffer = recs[0]
					self.userbuffer.append(wordbuffer)
					wordbuffer = ''

			# if ctl s, replace current with 2nd suggestion
			elif key == "\x13":
				if len(recs) > 1:
					wordbuffer = recs[1]
					self.userbuffer.append(wordbuffer)
					wordbuffer = ''

			# if ctl d, replace current with 3rd suggestion

			elif key == "\x04":
				if len(recs) > 2:
					wordbuffer = recs[2]
					self.userbuffer.append(wordbuffer)
					wordbuffer = ''
	
			# collect unwanted escape sequences and operators
			elif curses.ascii.isascii(key) == False:
				continue

			# add letter to word
			else:
				wordbuffer += key
			
			# generate recomendations based on current word
			# if a previous word exists, else assume null
			prev = ''
			if len(self.userbuffer) != 0:
				prev = self.userbuffer[-1]
			
			# only make suggestions for words once two chars are captured
			if len(wordbuffer) > 1:			
				recs = self.completions.shortRecs(prev, wordbuffer)
			else:
				recs = []


			#flatten to string for printing
			self.userview = ''
			for word in self.userbuffer:
				self.userview += (word + " ")
			self.userview += wordbuffer


			# clear console
			sys.stdout.write(u"\u001b[100D")
			sys.stdout.write(' ' * 400)
			sys.stdout.write(u"\u001b[1000D")
			sys.stdout.flush()

			#print new line to console
			sys.stdout.write("[]> "+ self.userview +"    "+ str(recs))
			sys.stdout.write(u"\u001b[" + str(len(str(recs)) + 4) + "D")
			sys.stdout.flush()
	
	# stop loop function, saves updated pickle to file
	def stop(self):
		print "Saving completions to file"
		output = open("completions.pkl", "wb")
		pickle.dump(self.completions, output)
		output.close()
		print "Quitting..."
		exit()

# pulls single char from stdin, allows for real time searching
def getch():
	# windows only
	try:
		import termios
	except:
		import msvcrt
		return msvcrt.getch()
	# unix systems
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)

	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return ch



if __name__ == "__main__":
	# load data into interface
	terminal = Interface("completions.pkl")

	# begin terminal loop
	terminal.start()
