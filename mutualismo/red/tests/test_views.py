from django.core import mail
from django.test import Client, TestCase

from red.managers import TradeManager
from red.models import Offer, Demand

class ViewTestCase(TestCase):
    """Helper class for testing views."""
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        self.url_prefix = ''
    
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

    def login(self):
        self.username = 'Alice'
        self.assertTrue(self.client.login(username='Alice', password='alice'))

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
    templates = ['base.html', 'index.html',]

    def setUp(self):
        ViewTestCase.setUp(self)
        self.trades = TradeManager()
        self.urls = self.create_urls([''])

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        # TODO test that, if we have any offer or demand to show, the proper 
        #      template is rendered
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestAbout(ViewTestCase):
    """About page."""
    templates = ['base.html', 'about.html',]

    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['about', 'about/'])

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestContact(ViewTestCase):
    """Contact page."""
    templates = ['base.html', 'contact.html', 'includes/form.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['contact', 'contact/'])

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_contact_form_post_templates(self):
        # when an invalid form is submitted, the contact page 
        # is rendered again
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'invalidemail',
                'cc_myself': True}
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, self.templates)

    def test_valid_contact_form_post_templates(self):
        # when a valid form is submitted, redirect to "thank you" page
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': True}
        templates = ['base.html', 'thankyou.html']
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, templates)

    def test_mail_to_admins_with_valid_contact_form_post(self):
        # without self CC
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': False}
        for url in self.urls:
            self.client.post(url, form)
            self.assertEqual(1, len(mail.outbox))
            cc_sender = mail.outbox[0].cc
            self.assertEqual(cc_sender, [])
            mail.outbox = []

    def test_mail_to_admins_and_user_with_valid_contact_form_post(self):
        # with self CC
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': True}
        for url in self.urls:
            self.client.post(url, form)
            self.assertEqual(1, len(mail.outbox))
            cc_sender = mail.outbox[0].cc[0]
            self.assertEqual(cc_sender, unicode(form['sender']))
            mail.outbox = []


class TestDashboard(ViewTestCase):
    """User's dashboard page."""
    templates = ['base.html', 'dashboard.html', 'includes/offer.html', 'includes/demand.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['dashboard', 'dashboard/'])
        self.login()

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestOffer(ViewTestCase):
    """Page for a certain offer."""
    templates = ['base.html', 'trade.html', 'includes/offer.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        offers = Offer.objects.all()
        self.urls = []
        for offer in offers:
            self.urls.append(offer.get_absolute_url())

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestDemand(ViewTestCase):
    """Page for a certain demand."""
    templates = ['base.html', 'trade.html', 'includes/demand.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        demands = Demand.objects.all()
        self.urls = []
        for demand in demands:
            self.urls.append(demand.get_absolute_url())

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestDeleteOffer(ViewTestCase):
    """Page for deleting a certain offer."""
    templates = ['base.html', 'dashboard.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.login()
        # offers for the user
        trades = TradeManager()
        self.offers = trades.offers(self.username) 
        # create urls
        self.urls = []
        for offer in self.offers:
            self.urls.append('/delete' + offer.get_absolute_url())

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_deletion(self):
        for offer in self.offers:
            slug  = offer.slug
            url = ('/delete' + offer.get_absolute_url())
            # get the offer to make sure that it exists
            Offer.objects.get(slug=slug)
            self.client.get(url)
            try:
                Offer.objects.get(slug=slug)
            except Offer.DoesNotExist:
                pass
            else:
                raise self.failureException("The offer had to be deleted")

    def test_http_not_found_if_offer_does_not_exist(self):
        url = '/delete/offer/random'
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)


class TestCreateService(ViewTestCase):
    """Page for creating or modifyng a certain service."""
    templates = ['base.html', 'create_service.html', 'includes/service_form.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.login()
        self.urls = ['/create/service', '/create/service/']

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_offer_form_post_templates(self):
        # when an invalid form is submitted, same templates are rendered again
        form = {'name': '',
                'description': '',}
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_offer_form_post_does_not_create_service(self):
        # when an invalid form is submitted the service is not created
        trades = TradeManager()
        user_services = trades.services(self.username) 
        expected_user_services = len(user_services)
        form = {'name': '',
                'description': '',}
        for url in self.urls:
            self.client.post(url, form)
            user_services = trades.services(self.username)
            self.assertEqual(expected_user_services, len(user_services))

    # FIXME
    #def test_valid_service_form_post_templates(self):
        ## when a valid form is submitted, dashboard templates are rendered
        #form = {'name': 'test',
                #'description': 'test',}
        #templates = ['base.html', 'dashboard.html', 'includes/service.html']
        #for url in self.urls:
            #response = self.client.post(url, form)
            #self.assertTemplatesUsed(response, templates)

    def test_valid_service_form_post_creates_service(self):
        # when a valid form is submitted the service is created
        trades = TradeManager()
        user_services = trades.services(self.username) 
        before_user_services = len(user_services)
        form = {'name': 'test',
                'description': 'test',}
        for url in self.urls:
            self.client.post(url, form)
            user_services = trades.services(self.username)
            self.assertEqual(before_user_services + 1, len(user_services))


class TestDeleteDemand(ViewTestCase):
    """Page for deleteing a certain demand."""
    templates = ['base.html', 'dashboard.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.login()
        # demands for the user
        trades = TradeManager()
        self.demands = trades.demands(self.username) 
        # create urls
        self.urls = []
        for demand in self.demands:
            self.urls.append('/delete' + demand.get_absolute_url())

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_deletion(self):
        for demand in self.demands:
            slug  = demand.slug
            url = ('/delete' + demand.get_absolute_url())
            # get the demand to make sure that it exists
            Demand.objects.get(slug=slug)
            self.client.get(url)
            try:
                Demand.objects.get(slug=slug)
            except Demand.DoesNotExist:
                pass
            else:
                raise self.failureException("The demand had to be deleted")

    def test_http_not_found_if_demand_does_not_exist(self):
        url = '/delete/demand/random'
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)


class TestCreateDemand(ViewTestCase):
    """Page for creating or modifyng a certain demand."""
    templates = ['base.html', 'create_demand.html', 'includes/demand_form.html']

    def setUp(self):
        ViewTestCase.setUp(self)
        self.login()
        # create urls
        self.urls = ['/create/demand', '/create/demand/']

    def test_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_demand_form_post_templates(self):
        # when an invalid form is submitted, same templates are rendered again
        form = {'name': '',
                'description': '',
                'trade_type': 0,}
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_demand_form_post_does_not_create_demand(self):
        # when an invalid form is submitted the demand is not created
        trades = TradeManager()
        user_demands = trades.demands(self.username) 
        expected_user_demands = len(user_demands)
        form = {'name': '',
                'description': '',
                'trade_type': 0,}
        for url in self.urls:
            self.client.post(url, form)
            user_demands = trades.demands(self.username)
            self.assertEqual(expected_user_demands, len(user_demands))

    # FIXME: test does not pass
    #def test_valid_demand_form_post_templates(self):
        ## when a valid form is submitted, dashboard templates are rendered
        #form = {'name': 'test',
                #'description': 'test',
                #'trade_type': 0,}
        #templates = ['base.html', 'dashboard.html', 'includes/demand.html']
        #for url in self.urls:
            #response = self.client.post(url, form)
            #self.assertTemplatesUsed(response, templates)

    def test_valid_demand_form_post_creates_demand(self):
        # when a valid form is submitted the demand is created
        trades = TradeManager()
        user_demands = trades.demands(self.username) 
        before_user_demands = len(user_demands)
        form = {'name': 'test',
                'description': 'test',
                'trade_type': 0,}
        for url in self.urls:
            self.client.post(url, form)
            user_demands = trades.demands(self.username)
            self.assertEqual(before_user_demands + 1, len(user_demands))
