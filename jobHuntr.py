#!/usr/bin/python


import argparse

import indeed

'''
-dependencies
-functions
	-sub function
	-main
-classes
-main
	-instantiated classes, instances, global variables
'''



#dependencies

#functions

#def search_indeed():




def main():
	parser = argparse.ArgumentParser(description="Template script tool")
	parser.add_argument('-f', help='takes arbitrary input')
	parser.add_argument('-b', action='store_true', help='binary flag')
	args=parser.parse_args()

	terms=open('terms.txt')
	areas=open('zipcodes.txt')
	for term in terms.readlines():
		for location in areas.readlines(): 
			results=indeed.search_indeed(term,2,int(location))
			print results
	terms.close()



class nullExample:	

	def __init__(self):
		internalVar='hello'

	def bar(self):
		print self.internalVar

class example():

        def __init__(self,var):
                self.internalVar=var



if __name__ == "__main__":
	foo = nullExample()
	bar = example('arbitrary object/value/pointer')
        main()
