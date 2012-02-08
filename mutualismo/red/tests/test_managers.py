from operator import attrgetter

from django.contrib.auth.models import User
from django.test import TestCase

from red.managers import TradeManager

class TradeManagerTest(TestCase):
    """Test case for ``TradeManager``."""
    fixtures = ['test.json']

    def setUp(self):
        self.manager = TradeManager()
    
    def test_latest_offers_count(self):
        count = 10
        latest_ten_offers = self.manager.latest_offers(count)
        self.assertLessEqual(len(latest_ten_offers), count)

    def test_latest_demands_count(self):
        count = 10
        latest_ten_demands = self.manager.latest_demands(count)
        self.assertLessEqual(len(latest_ten_demands), count)

    def test_latest_offer_count_when_negative(self):
        count = -3
        latest_offers = self.manager.latest_offers(count)
        self.assertEqual(0, len(latest_offers))

    def test_latest_demand_count_when_negative(self):
        count = -3
        latest_demands = self.manager.latest_demands(count)
        self.assertEqual(0, len(latest_demands))

    def test_latest_offers_sorted_by_date(self):
        latest_offers = self.manager.latest_offers()
        self.assertEqual(latest_offers, sorted(latest_offers, 
                                               key=attrgetter('date'),
                                               reverse=True))

    def test_latest_demands_sorted_by_date(self):
        latest_offers = self.manager.latest_offers()
        self.assertEqual(latest_offers, sorted(latest_offers, 
                                               key=attrgetter('date'),
                                               reverse=True))

    def test_user_offers(self):
        alice = User.objects.get(username=u'Alice')
        offers = self.manager.offers(alice)
        for offer in offers:
            self.assertEqual(offer.owner, alice)

    def test_user_demands(self):
        alice = User.objects.get(username=u'Alice')
        demands = self.manager.demands(alice)
        for demand in demands:
            self.assertEqual(demand.owner, alice)
