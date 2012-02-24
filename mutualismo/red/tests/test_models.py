from django.test import TestCase

from red.models import Offer, Demand, Loan


class TestOffer(TestCase):
    """Test ``Offer`` class."""
    fixtures = ['test.json']

    def setUp(self):
        self.offers = Offer.objects.all()

    def test_get_absolute_url(self):
        URL_PREFIX = '/offer'
        for offer in self.offers:
            expected_url = '/'.join([URL_PREFIX, offer.slug])
            returned_url = unicode(offer.get_absolute_url())
            self.assertEqual(expected_url, returned_url)


class TestDemand(TestCase):
    """Test ``Demand`` class."""
    fixtures = ['test.json']

    def setUp(self):
        self.demands = Demand.objects.all()

    def test_get_absolute_url(self):
        URL_PREFIX = '/demand'
        for demand in self.demands:
            expected_url = '/'.join([URL_PREFIX, demand.slug])
            returned_url = unicode(demand.get_absolute_url())
            self.assertEqual(expected_url, returned_url)

    def test_type_for_humans(self):
        code_string = {}
        for code, string in Demand.TYPE_CHOICES:
            code_string[code] = string
        for demand in self.demands:
            self.assertEqual(demand.type_for_humans(), code_string[demand.trade_type])


class TestLoan(TestCase):
    """Test ``Demand`` class."""
    fixtures = ['test.json']

    def setUp(self):
        self.loans = Loan.objects.all()

    def test_status_for_humans(self):
        code_string = {}
        for code, string in Loan.STATUS_CHOICES:
            code_string[code] = string
        for loan in self.loans:
            self.assertEqual(loan.status_for_humans(), code_string[loan.status])

