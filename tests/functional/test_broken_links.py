''' Crawl the running Docker site and verify all links give a 200 OK '''

import unittest
import re
import requests

class BrokenLinkTest(unittest.TestCase):
    ''' Base class for testing links '''

    def setUp(self):
        ''' Define some unique data for validation '''
        self.domain = "http://127.0.0.1"
        self.acceptable_codes = [200]

    def tearDown(self):
        ''' Destroy unique data '''
        self.domain = None
        self.acceptable_codes = None

    def request_recurse(self, url=None, requested=None):
        ''' Recursively request each page checking the return code and grabbing URL's from HTML '''
        code_counts = {}
        if requested is None:
            requested = []
        if url in requested:
            return code_counts, requested
        else:
            requested.append(url)
        url = self.domain + url
        results = requests.get(url, allow_redirects=False, verify=False)
        if results.status_code in code_counts:
            code_counts[results.status_code] = code_counts[results.status_code] + 1
        else:
            code_counts[results.status_code] = 1
        urls = re.findall(
            'href="/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            results.text
        )
        for url in urls:
            url = url.lstrip('href="')
            if "//" not in url:
                results, requested = self.request_recurse(url, requested=requested)
                # Increment counts for status codes
                for key in results.keys():
                    if key in code_counts:
                        code_counts[key] = code_counts[key] + results[key]
                    else:
                        code_counts[key] = results[key]
        return code_counts, requested

class CrawlSite(BrokenLinkTest):
    ''' Verify no broken links are present within blog '''
    def runTest(self):
        ''' Execute recursive request '''
        results, requested_pages = self.request_recurse("/")
        for key in results.keys():
            self.assertTrue(
                key in self.acceptable_codes,
                "Found {0} in return codes with a count of {1}".format(key, results[key])
            )
