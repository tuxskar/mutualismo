from django.test import Client, TestCase


class UrlTestCase(TestCase):
    """Helper class for testing URLs."""
    def setUp(self):
        self.client = Client()

    def assertHttpOk(self, url):
        """Checks that the given URL returns a 200 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestURLs(UrlTestCase):
    def test_index_ok(self):
        urls = ['', '/']
        for url in urls:
            self.assertHttpOk(url)

