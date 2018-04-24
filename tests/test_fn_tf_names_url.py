# 3. fn/tf/names_url

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, "TaxonFinder_wrapper_url","fn/tf/names_url")

class TestFnNamesUrl(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """Test a call with No parameters.
        """

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue('Missing parameter "url" in "%s"' % x.json()[u'message'])
        #self.assertTrue(u'url' in x.json()[u'message'], 'Missing parameter "url" in "%s"' % x.json()[u'message'])

    def test_non_http_uri(self):
        """Test a Non-HTTP URI as parameter.
        """

        request = service.get_request('GET', {u'url': u'urn:nbn:de:bvb:19-146642'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)

    def test_nonexistent(self):
        """Test a Non-existent URI as parameter.
        """

        request = service.get_request('GET', {u'url': u'https://example.com/nonexistent.txt'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)
        # TBD: test for informative message

    
    def test_edge_case(self):
        """Test edge case: parameter name 'url' is supplied, but there is no value.
        """

        request = service.get_request('GET', {u'url': u''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)
        
    def test_bad_type(self):
        """Test url of an unrecognized type file as parameter value.
        It succeeds with no results.  I would think that GNRD should have told
        us that the file couldn't be processed, but it doesn't.
        There is no way to distinguish in the GNRD response the absence of names
        from an invalid file, so not sure what we should expect here.
        TBD: GNRD issue.
        NOTE: If this URL stops working, simply replace it by any other
        similar URL on the web - a zip or tarball, or even an image."""

        request = service.get_request('GET', {u'url': u'http://files.opentreeoflife.org/silva/silva-115/silva-115.tgz'})
        x = self.start_request_tests(request)
        self.assertEqual(x.json()[u'scientificNames'], [])

    @unittest.skip("temporarily to save time (takes 4 minutes)")
    def test_large_input(self):
        """Test large input.
        This takes 240 seconds (4 minutes) on a 10 Mb input file - but it works."""

        # TBD: where should this file be located?  Github?
        request = service.get_request('GET', {u'url': u'https://github.com/jar398/tryphy/raw/master/some-names.txt'})
        print >>sys.stderr, '\nBe patient, takes four minutes'
        x = self.start_request_tests(request)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 1000)
    
    def test_example_1(self):
        """Test example_1 from the documentation."""

        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 20)
        self.assertTrue(u'Camponotus sericeus' in x.json()[u'scientificNames'])


    def test_example_2(self):
        """Test example_2 from the documentation."""

        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 5)
        self.assertTrue(u'Macaca sinica' in x.json()[u'scientificNames'])

null=None; false=False; true=True

example_1 = service.get_request('GET', {u'url': u'http://en.wikipedia.org/wiki/Ant'})
example_2 = service.get_request('GET', {u'url': u'https://en.wikipedia.org/wiki/Monkey'})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================TaxonFinder_wrapper_url=========================' 
    webapp.main()
