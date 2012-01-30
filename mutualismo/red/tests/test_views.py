from django.test import Client, TestCase


class TestIndex(ViewTestCase):
    def setUp(self):
        self.client = Client()

    def test_templates(self):
        urls = ['', '/']
        responses = [self.client.get(url) for url in urls]
        templates = ['base.html', 'index.html']
        for response in responses:
            for template in templates:
                self.assertTemplateUsed(response, template)
