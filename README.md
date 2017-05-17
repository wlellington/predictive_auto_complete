# Predictive Auto Complete
A simple Auto Complete tool for python applications

Wesley Ellington
CSE 3353
Fundamental of Algorithms

## In a nut shell

	* Created a custom Trie data structure
	* Wrote a parser to feed in a corpus of text to create suggestions
	* Built a search tool for the Trie in real time to generate ranked
 		suggestions based on prefix and context
	* Implemented a method to return top results to user for them to select
	* Designed a simulated Command Interface for demonstration


## Blueprint

For this project, I have decided to implement an adaptive auto complete
system that can be purposed for many applications. It will make used of 
a large trie data structure that will read in a corpus of text to serve
as its initial training state. It will make completion recommendations 
to the used in real time as they type, and will make use of simple 
context information to better help the user as they type.

The goal of this is to build a general purpose set of classes and 
functions that can be integrated into other systems. For example, one
could use this as wrapper around BASH to help the user get completion
recommendations, or in vim to learn common function names when programming.
With all of this in mind, it will be open and deployable.

For demonstration purposes, I will construct a simple command line like
interface that will be able to interact with the trie and output results
in real time.



# Implementation

The most straight forward method I found for implementing a trie was to use
a special version of the basic Python dictionary in the collections module.
Known as defaultdict, it allows the user to get around missing key errors
and initialize key value pairs that may not exist, rather than returning 
errors.

Once built, I needed to add a few extra bells and whistles to make searching
the tree easier. This included a method of returning all results on a prefix 
search with associated word frequencies to better support scoring. This was 
done by implementing a depth first search on the trie implementation that 
I created. This allows me to easily scale returned scores based on history
info for ranking suggestions. Both the parser and the demo interface output
the stored trie object to a Python pickle so that we can easily reload our 
information later.

One of the largest struggles however, was dealing with the realtime typing
issue for the interface. Because stdin typically needs a return character 
'\r' to send input to a waiting program, I had to find a way of going around
typical input means. I found a very helpful post that explained how one could
implement a get character function to pull key strokes from console easily.

It should be mentioned that the recommendations are based purely on the
documents fed into the trie initially. This means that any language that is
read left to right with whitespacing can be used as input. Code is no
exception and the system should be able to start understanding syntax with
time.



## Results

Overall, I am pretty happy with the results I was able to achieve. Initially,
I had hoped to get this program to interface with BASH or vim so that I could
begin using it, but limitations in my OS knowledge kept me from making it that
far. A pleasant supprise came when testing the previous to current word 
associations, as the structure was able to learn much faster than I had 
anticipated. I now see several optimizations that I could have made to save
time and space in my trie. I have faith that I did succeed in my goal of 
deployability, and should I write a python CLI, or borrow one such as the 
critically acclaimed f\*\*k (yes thats what it is called) CLI for command 
correction, my program would scale nicely with little to no modification.
One cutback I did need to make was that my search time on prefixes of less
than two chars took a considerable time, making the interface almost unusable.
To combat this, my system will now only begin making suggestions once two 
letters have been entered.



## Moving Forward

As stated above, I would like to see actual use of my project in my development 
environment. If I had more time to work, I would take the demo interface I have 
constructed, and add a full implementation of some method to speak to BASH, or
whatever task is running underneath it. This would probably require some sort
of multi threading for both the underlying process, and possibly the prefix 
searching for better speed.
