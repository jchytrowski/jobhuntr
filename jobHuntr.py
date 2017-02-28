#!/usr/bin/python


import argparse

import indeed


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
		

	for jobset in main_list:
		for listing in jobset:
			title=jobset[listing][0]
			url=jobset[listing][1]
			location=jobset[listing][2]
			snippet=jobset[listing][3]
			company=jobset[listing][4]
			print '''%s 
%s  -- %s
%s
%s

''' % (title, company, location, snippet, url)		

if __name__ == "__main__":
        main()
