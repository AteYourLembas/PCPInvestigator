import time, sys, datetime, json
from collections import defaultdict
import optparse

from pymongo import Connection

from bs4 import BeautifulSoup
import urllib, urllib2
from urllib2 import urlopen

import PCPSites
import PCPConstants as CONSTANTS

connection = Connection(CONSTANTS.DB_HOST, CONSTANTS.DB_PORT) # default port for mongo
db = connection.test 	# attach to test db
providers = db.providers # get handle for providers


SEARCH_TOOL = "https://www.google.com"

SOURCE_SITES = [PCPSites.HealthGrades,
				PCPSites.Vitals,
				PCPSites.UCompareHealthCare,
				PCPSites.Yelp
				]



############################################################# 
#############################################################
######## PCPScraper
############################################################# 
############################################################# 

class PCPScraper(object) :


	def __init__(self):
		
		self.dryrun = False
		self.parsedOptions = None	

		self._loadOptions()


	####################################################################
	# _loadOptions
	####################################################################	
	def _loadOptions(self):	
	
		self.options = optparse.OptionParser()

		self.options.add_option("-d", "--dryrun", action="store_true", default=False, 
							help="Simulate and generate output for first five entries. Do not add to database.")

	######################################
	# scrapeSearch
	######################################
	def scrapeSearch(self, firstname, middlename, lastname, title, moveonIfFail=True) :
		"""
		Action:		Perform search for provider and return all resulting links
		
		"""	

		# Number of results to search for (20 usually gets us what we want)
		#
		maxResults = 20

		# Perform search
		#	
		firstname = firstname if not middlename else "%s+%s"%(firstname, middlename)
		query = "%s+%s+%s+reviews"%(firstname, lastname, title)

		#print "query %s"%query

		# Scrape all links in the results
		#
		address = "%s/search?q=%s&num=%s&hl=en&start=0" % (SEARCH_TOOL, urllib.quote_plus(query), maxResults)

		#print "Address %s"%address

		request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})

		try :

			urlfile = urllib2.urlopen(request)

		except urllib2.HTTPError, e :

			print "Hit an HTTPError %s. Retrying..."%e
			time.sleep(CONSTANTS.SEARCH_SLEEPTIME)
			if moveonIfFail :
				return self.scrapeSearch(firstname, middlename, lastname, title, moveonIfFail=False)
			else :
				return []


		page = urlfile.read()

		#print "Page: %s"%page

		soup = BeautifulSoup(page, 'html.parser')

		allLinks = []
		for h3 in soup.findAll('h3', attrs={'class':'r'}):
			#print "h3: %s"%h3
			sLink = h3.find('a')
			#print "sLink %s"%sLink['href']
			allLinks.append(sLink['href'])

		return allLinks


	######################################
	# loadSites
	######################################
	def loadSites(self, searchResults, lastname) :
		"""
		Action:		From a list of URLs, return the URLs we're interested in
		
		"""	

		loadedSites = []

		for siteclass in SOURCE_SITES :

			for sourcepath in searchResults :

				# Verify that the URL is from a source we like and has the given last name in the URL
				# This is not foolproof, but we'll do a better sanity check when we scrape
				#
				if sourcepath.startswith(siteclass.URL) and lastname.lower() in sourcepath.lower() :

					loadedSites.append(siteclass(sourcepath))

		return loadedSites



	######################################
	# parseOptions
	######################################
	def parseOptions(self, options) :

		self.parsedOptions = None	
		(self.parsedOptions, self.remaining) = self.options.parse_args(list(options))

		if getattr(self.parsedOptions, "dryrun") :
			self.dryrun = self.parsedOptions.dryrun


	######################################
	# runAction
	######################################
	def runAction(self) :

		# Gather providers from database
		# that have no lastscraped
		#
		count = db.command({ "count":'providers', "query": { "lastscraped": { "$in": ["", 0, None] } }})["n"]

		#count = db.command({ "count":'providers', "query": { "lastscraped": { "$exists": False } }})["n"]

		providerObjs = providers.find( { "lastscraped": { "$in": ["", 0, None] } } , timeout=False)

		samplesize = 3 if self.dryrun else int(count)

		print "Searching for %s providers..."%count

		for providerObj in providerObjs : 

			time.sleep(CONSTANTS.SEARCH_SLEEPTIME)

			# Proceed only if we have found a name to search for
			#
			if "lastname" in providerObj :

				# Fetch dict of form {"vitals": "http://...."}
				#
				print "------------------------------------------------------------"
				print "*** SEARCHING for %s ***"%([providerObj["firstname"], providerObj["middlename"], providerObj["lastname"], providerObj["title"]])
				print "------------------------------------------------------------"

				searchResults = self.scrapeSearch(providerObj["firstname"], providerObj["middlename"], providerObj["lastname"], providerObj["title"])
				sites = self.loadSites(searchResults, providerObj["lastname"])

				print "FOUND POTENTIAL SITES: " + str([site.NICKNAME for site in sites])

				ratings = []
				completedSites = []

				for site in sites :

					# If we already scraped this site, move on
					#
					if site.NICKNAME in completedSites :
						continue

					time.sleep(CONSTANTS.SITE_SLEEPTIME)

					print "SCRAPING SITE %s via %s..."%(site.NICKNAME, site.sourcePath)

					# Verify that first, last and title (e.g. MD, DDS) are in the business name of the site
					#
					nameTermsToVerify = [providerObj["firstname"], providerObj["lastname"], providerObj["title"]]

					scrapeSuccessful = site.scrape(nameTerms=nameTermsToVerify)

					# If our scrape succeeded,
					# we can check this site off the list
					#
					if scrapeSuccessful :

						print "--------------------------"
						print "%s RESULTS: %s"%(site.NICKNAME, str([site.overallscore, site.summary, site.numreviews, json.dumps(site.reviews)]))
						print "--------------------------"

						ratings.append({"sourcetype": site.NICKNAME,
									"path": site.sourcePath,
									"overallscore": site.overallscore,
									"numreviews": site.numreviews, 
									"summary": site.summary,
									"reviews": site.reviews})

						completedSites.append(site.NICKNAME)

					else :

						print "SCRAPE FAILED. PROVIDER MISMATCH OR NO REVIEWS?"

					print "--------------------------"


				providerObj["ratings"] = ratings
				providerObj["lastscraped"] = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
				
				if not self.dryrun :

					print "--------------------------"
					print "*** SAVING results of %s to %s %s %s ***"%(completedSites, providerObj["firstname"], providerObj["lastname"], providerObj["title"])
					print providerObj
					providers.save(providerObj)
					print "*** DONE SAVING ***"
					print "--------------------------"

				print "------------------------------------------------------------"




######################################
# Main action
######################################

if __name__ == '__main__':

	options = sys.argv
	workingObj = PCPScraper()
	workingObj.parseOptions(options)
	status = workingObj.runAction()		
 	sys.exit(status)
