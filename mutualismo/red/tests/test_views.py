from django.test import Client, TestCase


class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()

    def test_templates(self):
        urls = ['', '/']
        responses = [self.client.get(url) for url in urls]
        templates = ['base.html', 'index.html']
        for response in responses:
            for template in templates:
                self.assertTemplateUsed(response, template)


class TestAbout(TestCase):
    def setUp(self):
        self.client = Client()

    def test_templates(self):
        #FIXME: works in the server but the test fails
        urls = ['about', 'about/']
        responses = [self.client.get(url) for url in urls]
        templates = ['base.html', 'about.html']
        for response in responses:
            for template in templates:
                self.assertTemplateUsed(response, template)
