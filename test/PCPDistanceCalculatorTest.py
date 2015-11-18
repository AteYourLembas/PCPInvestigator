#!/usr/bin/python

import unittest, os, sys, testUtil

import PCPDistanceCalculator

class PCPDistanceCalculatorTest(testUtil.commonTest):
	
	
	def setUp(self):
		
		pass

	def tearDown(self):

		pass
		
		
	def _setUp(self):

		pass


	def _tearDown(self):

		pass



	def testGetDistance(self) :

		providerAddress = {}
		providerAddress["address1"] = "1125 South Beverly Drive"
		providerAddress["address2"] = "Suite 601"
		providerAddress["address3"] = "Los Angeles, CA 90035"
		providerAddress["address4"] = "(310) 277-3762"


		homeZip = "90066"
		awayZip = "90232"

		us = 2.3
		them = PCPDistanceCalculator.getDistance(homeZip, awayZip)
		self._compare(str(us), str(them))


		awayZip = "27614"

		us = 2748.7
		them = PCPDistanceCalculator.getDistance(homeZip, awayZip)
		self._compare(str(us), str(them))


		awayZip = "90401"

		us = 4.2
		them = PCPDistanceCalculator.getDistance(homeZip, awayZip)
		self._compare(str(us), str(them))


		awayZip = "90066"

		us = 0.0
		them = PCPDistanceCalculator.getDistance(homeZip, awayZip)
		self._compare(str(us), str(them))



		awayZip = "junk"

		us = "Unknown"
		them = PCPDistanceCalculator.getDistance(homeZip, awayZip)
		self._compare(str(us), str(them))
	

if __name__ == "__main__":
	unittest.main()