from django.test import Client, TestCase

class UrlTestCase(TestCase):
    """Helper class for testing URLs."""
    def setUp(self):
        self.client = Client()

    def assertHTTPOk(self, url):
        """Checks that the given URL returns a 200 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestURLs(UrlTestCase):
    url_prefix = '/red'

    def create_urls(self, urls):
        return ['/'.join([self.url_prefix, url]) for url in urls]

    def test_create_urls_correct(self):
        urls = ['', 'about/', 'contact']
        created_urls = self.create_urls(urls)
        # same number of elements
        self.assertEqual(len(urls), len(created_urls))
        # with the url prefix for the application
        original_and_created_urls = zip(urls, created_urls)
        for original, created in original_and_created_urls:
            self.assertEqual(self.url_prefix + '/' + original, created)
        
    def test_index_http_ok(self):
        urls = self.create_urls([''])
        for url in urls:
            self.assertHTTPOk(url)

    def test_about_http_ok(self):
        urls = self.create_urls(['about', 'about/'])
        for url in urls:
            self.assertHTTPOk(url)
