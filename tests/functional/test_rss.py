''' Grab the RSS feed (test 1) and loop through each article
 then ensure title, link and description exist'''
import unittest
import feedparser

class ContentTest(unittest.TestCase):
    ''' Run a unit test against load_post_config() '''

    def setUp(self):
        ''' Create a pseudo environment for function to run '''
        self.domain = "feed.bencane.com"
        self.url = "http://127.0.0.1"

    def tearDown(self):
        ''' Destroy pseudo environment for next run '''
        self.url = None
        self.domain = None

class VerifyRSS(ContentTest):
    ''' Verify no broken links are present within blog '''
    def runTest(self):
        ''' Execute recursive request '''
        feed = feedparser.parse(self.url, request_headers={'host' : self.domain})
        for item in feed.entries:
            self.assertIsNotNone(item.title, "Could not find title within RSS item")
            self.assertIsNotNone(item.link, "Could not find link within RSS item")
            self.assertIsNotNone(item.description, "Could not find description within RSS item")
