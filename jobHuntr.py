#!/usr/bin/python


import argparse
import pickle
import indeed
import os.path
import notifier

class archive:

	# an archive is useful if we want to run this as a chron job, and dont
	# want prior results displayed again
	# Eventually, maybe we'll figure out a low effort means of tracking 
	# what i've actually applied to or dismissed, instead of just 'viewed'	

        def __init__(self):
		self.class_archive={}
		if os.path.isfile('archive.pkl'):
			with open('archive.pkl', 'r') as file:
				self.class_archive=pickle.load(file)	

			i=0
			for key in self.class_archive.keys():
				i+=1			
	

        def push_archive(self,url):
		self.class_archive[str(url)]=True

	def query_archive(self,url):

		if url in self.class_archive:
			'''kinda redundant; we only store true, so if there- 
			is a key, then that implies the key is True; still,
			simply checking for the existance of a key seems sloppy.
			This way, we can later revert values to false 
			(in case we want to later revert/change behavior,
			or perhaps store a 'last viewed' instead of a bool?)
			'''
			
			return self.class_archive[url]
		else:
			return False


	def commit(self):
		with open('archive.pkl', 'w') as handle:
			pickle.dump(self.class_archive,handle)



def thresher(listings, filter_terms):
        #removing entries from listing
        assert type(listings) is dict
        assert type(filter_terms) is list
        chaff=[]
        for listing in listings:
		assert type(listings[listing]) is list
                if any (term in listings[listing][0] for term in filter_terms):
                        chaff.append(listing)
        for trash in chaff:
                del listings[trash]

        return listings


def main():

	main_list=[]
	#just in case I want to add flags later...
	parser = argparse.ArgumentParser(description="Template script tool")
	parser.add_argument('-f', help='takes arbitrary input')
	parser.add_argument('-b', action='store_true', help='binary flag')
	args=parser.parse_args()

	#lets keep track of what we've already applied to	
	history=archive()	

	filter_terms=open('filter_terms.txt')	
	search_terms=open('terms.txt')
	areas=open('zipcodes.txt')
	filter_terms_list=[]
	
	for term in filter_terms.read().splitlines():
		filter_terms_list.append(term)

	for term in search_terms.readlines():
		for location in areas.readlines(): 
			results=indeed.search_indeed(term,2,int(location))
			results=thresher(results,filter_terms_list)
			main_list.append(results)

	filter_terms.close()
	search_terms.close()
	areas.close()
		
	
	notifier.sendNotice(main_list,history)
#	for jobset in main_list:q
#		for listing in jobset:
#			title=jobset[listing][0]
#			url=jobset[listing][1]
#			location=jobset[listing][2]
#			snippet=jobset[listing][3]
#			company=jobset[listing][4]
#
#			if history.query_archive(url):
#				continue
#			else:
#				history.push_archive(url)
#
#			print '%s \n%s  -- %s\n%s\n%s\n\n' % (title, company, location, snippet, url)		

	#save
	history.commit()	


if __name__ == "__main__":
        main()
