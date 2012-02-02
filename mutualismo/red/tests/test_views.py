from django.test import Client, TestCase

class ViewTestCase(TestCase):
    """Helper class for testing URLs."""
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        self.url_prefix = '/red'
    
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

    def assertHTTPOk(self, url):
        """Checks that the given URL returns a 200 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def assertTemplatesUsed(self, response, templates):
        """
        Checks that every template in ``template`` was rendered 
        in ``response``.
        """
        for template in templates:
            self.assertTemplateUsed(response, template)


class TestIndex(ViewTestCase):
    """Index page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls([''])
        self.templates = ['base.html', 'index.html']

    def test_index_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestAbout(ViewTestCase):
    """About page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['about', 'about/'])
        self.templates = ['base.html', 'about.html']

    def test_about_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

class TestContact(ViewTestCase):
    """Contact page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['contact', 'contact/'])
        self.templates = ['base.html', 'contact.html']

    def test_about_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)
