#!/usr/bin/python

import unittest, os, sys, testUtil

from PCPSites import HealthGrades, Vitals, UCompareHealthCare, Yelp

class PCPSitesTest(testUtil.commonTest):
	
	
	def setUp(self):
		
		pass

	def tearDown(self):

		pass
		
		
	def _setUp(self):

		pass


	def _tearDown(self):

		pass




	def testHealthGrades(self):

		healthGrades = HealthGrades()
		html = open("input/healthgrades_sample_20151115.html", 'r').read()
		healthGrades._scrape(html, nameTerms=['Vinay', 'Aggarwal', 'MD'])

		self._compare(str(0.84), str(healthGrades.overallscore)) # 1 = 100%
		self._compare(5, healthGrades.numreviews)

		expectedReviews = [{'score': 0.92, 'overalldescription': '', 'comments': [], 'title': u'Ease of scheduling urgent appointments'}, {'score': 0.92, 'overalldescription': '', 'comments': [], 'title': u'Office environment, cleanliness, comfort, etc.'}, {'score': 0.96, 'overalldescription': '', 'comments': [], 'title': u'Staff friendliness and courteousness'}, {'score': None, 'overalldescription': '', 'comments': [], 'title': u'Total wait time (waiting & exam rooms)'}, {'score': 0.84, 'overalldescription': '', 'comments': [], 'title': u"Level of trust in provider's decisions"}, {'score': 0.84, 'overalldescription': '', 'comments': [], 'title': u'How well provider explains medical condition(s)'}, {'score': 0.84, 'overalldescription': '', 'comments': [], 'title': u'How well provider listens and answers questions'}, {'score': 0.88, 'overalldescription': '', 'comments': [], 'title': u'Spends appropriate amount of time with patients'}]
		self._compare(expectedReviews, healthGrades.reviews)





	def testUCompareHealthCare(self) :


		ucomparehealthcare = UCompareHealthCare()
		html = open("input/ucomparehealthcare_sample_20151115.html", 'r').read()
		ucomparehealthcare._scrape(html, nameTerms=['Phabillia', 'Afflack', 'MD'])

		self._compare(1.0, ucomparehealthcare.overallscore) # 1 = 100%
		self._compare(1, ucomparehealthcare.numreviews)

		expectedReviews = [{'date': '2011-02-07', 'score': 1.0, 'overalldescription': u'Excellent', 'comments': [], 'title': None}]
		self._compare(expectedReviews, ucomparehealthcare.reviews)



	def testVitals(self) :


		vitals = Vitals()
		html = open("input/vitals_sample_20151115.html", 'r').read()
		vitals._scrape(html, nameTerms=['Shahram', 'Abrishamy', 'MD'])

		self._compare(1.0, vitals.overallscore) # 1 = 100%
		self._compare(4, vitals.numreviews)

		expectedReviews = [{'date': '2013-06-11', 'score': 1.0, 'overalldescription': '', 'comments': [u"I've seen Dr. Abrishamy several times over the years and he never disappoints.  Great bedside manner, explains problems, caring, and knowledgable.  Everything a Doctor should be!! "], 'title': u'Great Experience!  '}]
		self._compare(expectedReviews, vitals.reviews)



	def testYelp(self) :


		yelp = Yelp()
		html = open("input/yelp_sample_20151115.html", 'r').read()
		yelp._scrape(html, nameTerms=['Nusinovich', 'Vlad', 'MD'])

		self._compare(0.8, yelp.overallscore) # 1 = 100%
		self._compare(20, yelp.numreviews)

		expectedReviews = [{'date': '2015-07-30', 'score': 1.0, 'overalldescription': '', 'comments': [u'This Dr is amazing!! The entire staff is very helpful and nice. Sasha and Masha (front desk) are awesome they are alway sweet and pleasant!! Strongly recommend'], 'title': ''}, {'date': '2015-10-08', 'score': 0.2, 'overalldescription': '', 'comments': [u"If I could put 0 - I would. If you want doctor who don't care go for it! Majority of reviews here are fake: young folks from over the city. His primary clientele in Russian community. He never available in office- all medical task are provided by nurse practitioner. He never call back. His NP can call you(!) in 2-3 days to find what is going on with patient. So, if you need doctor who don't care- doctor Vlad is your choice."], 'title': ''}, {'date': '2013-11-10', 'score': 1.0, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2014-06-02', 'score': 1.0, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2015-01-08', 'score': 1.0, 'overalldescription': '', 'comments': [u"I can't recommend Dr. Nusinovich enough!  He will go above and beyond for his patients, day and night!  He's very thorough and efficient, and will make sure you're in good hands.  The staff is so wonderful too.  His office is located in the Whole Foods complex and is very easy to find!"], 'title': ''}, {'date': '2014-09-23', 'score': 0.2, 'overalldescription': '', 'comments': [u'Awful place to see a doctor'], 'title': ''}, {'date': '2014-02-17', 'score': 1.0, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2013-10-16', 'score': 0.2, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2013-12-14', 'score': 1.0, 'overalldescription': '', 'comments': [u'Beautiful Office! Great Service! Professional Staff!'], 'title': ''}, {'date': '2014-07-17', 'score': 1.0, 'overalldescription': '', 'comments': [u"He's the best. He put me at ease, listened attentively and was extremely kind and knowledgeable."], 'title': ''}, {'date': '2014-07-17', 'score': 1.0, 'overalldescription': '', 'comments': [u'Excellent Doctor highly recommend very professional and knowledgeable doctor! A true healer of the medical field! Thank You Dr Nusinovich!'], 'title': ''}, {'date': '2013-11-09', 'score': 1.0, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2013-11-09', 'score': 1.0, 'overalldescription': '', 'comments': [u'Dr. Nusinovich, Vlad is a remarkable physician. He took his time doing a thorough examination and his office is very clean and his staff is very polite and courteous. I never have to wait longer than 5-10 minutes to be seen and his knowledge and expertise makes it comfortable for me to make him my PCP as I have had open-heart surgery and need an educated MD by my side due to my condition. Its been 5 years and I am looking forward to having Vlad be my MD for the rest of my life. Highly recommended.'], 'title': ''}, {'date': '2013-10-03', 'score': 0.2, 'overalldescription': '', 'comments': [None], 'title': ''}, {'date': '2013-11-10', 'score': 1.0, 'overalldescription': '', 'comments': [u"I can not even begin to express how amazing,Kind,Efficient, and caring Dr.Nusinovich is..All the way down to the sweet ladies at the front desk! I have been going to see him now for about 2 years and I feel like Family:) I often have to leave out if town for work,and it's hard for me to make an appointment ahead of time,But Dr.Nusinovich has always worked me in with out hesitation! I am so happy I found You!!"], 'title': ''}, {'date': '2014-05-02', 'score': 0.2, 'overalldescription': '', 'comments': [u'I\'ve never seen Dr. Vlad. You will most likely be seen by a nurse practitioner. The nurse practitioners that I dealt with were very nice. However, the front desk staff is incompetent. It\'s always a frustration when dealing with the front desk staff. Most recently, I called to get a referral to a specialist for a follow up. I called and explained and she said she would call me back on whether I would need another referral since I have already been to the doctor (which is something I feel they should already know, but I dont work in Dr. office). An hour passes by so I decided to call the specialist\'s office and they told me I would need another referral as well as a fax referral. I call back because I wanted to see if she had checked as well as to give them the fax information. She says "Didn\'t I speak to you earlier" and I say yes I didn\'t get a call back she replies rudely "Yeah but not in 5 or 10 minutes, (laughs) more like the end of the day." FIrst of all it was not even close to 10 minutes. Secondly, how was I supposed to know she would call end of day when she never told me when she would call me back. I told her not to be rude. Not the first time I\'ve experience rudeness/incompetence from that office but that incidence compelled me to write this review.  I\'ll be changing doctors, one that I\'ll actually get to meet.'], 'title': ''}, {'date': '2013-11-12', 'score': 0.2, 'overalldescription': '', 'comments': [u'I know the doctor and he seems like a good person, but this place is a waste. I wasted a number of years on sub-par services, medically and administratively speaking. It was pathetic.'], 'title': ''}, {'date': '2013-11-19', 'score': 1.0, 'overalldescription': '', 'comments': [u'This place is awesome! The girls at the front desk are amazing. I have been going there for 4 years. I love this dr!'], 'title': ''}, {'date': '2013-11-08', 'score': 1.0, 'overalldescription': '', 'comments': [u'I have been seeing Dr. Nusinovich for the last three years. His office is clean and his staff is courteous. I never have to wait longer than 10 minutes from my scheduled appointment time, which is very convenient and important to me. I am a busy trial attorney and deal with doctors often and I think Dr. Nusinovich  is one of the best. Five stars all the way.'], 'title': ''}, {'date': '2013-11-09', 'score': 1.0, 'overalldescription': '', 'comments': [u'I love this place! Dr. Vlad and the nurses are so sweet. I hope my insurance never changes ! So I can always go to them.'], 'title': ''}]
		self._compare(expectedReviews, yelp.reviews)
	

if __name__ == "__main__":
	unittest.main()