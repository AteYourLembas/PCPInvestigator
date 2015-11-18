#!/usr/bin/python

import unittest, sys



class commonTest(unittest.TestCase):


	def _compare(self, us, them):
		assert us == them, "Expected " + str(us) + " but was " + str(them)	
			
	
	def _compareDicts(self, dict1, dict2):
		
		assert len(dict1) == len(dict2), "Dicts not the same length : expected length " + str(len(dict1)) + " but was " + str(len(dict2))
		
		for key in dict1.iterkeys() :
			assert key in dict2.iterkeys(), "Key " + str(key) + " not found in 'them' set"
			assert dict1[key] == dict2[key], "For key " + str(key) + " expected value " + str(dict1[key]) + " but was " + str(dict2[key])


	def _compareLists(self, list1, list2):

		assert len(list1) == len(list2), "Lists not the same length : expected length " + str(len(list1)) + " but was " + str(len(list2))

		for i in range(0, len(list1)) :
			assert list1[i].__eq__(list2[i]), "For item of index " + str(i) + " expected entry " + str(list1[i].__str__()) + " but was " + str(list2[i].__str__())
	

	def _sortAndCompareLists(self, list1, list2):
	
		assert len(list1) == len(list2), "Lists not the same length : expected length " + str(len(list1)) + " but was " + str(len(list2))		
		
		list1.sort()
		list2.sort()
		
		for i in range(0, len(list1)) :
			assert list1[i].__eq__(list2[i]), "For item of index " + str(i) + " expected entry " + str(list1[i].__str__()) + " but was " + str(list2[i].__str__())
		
	