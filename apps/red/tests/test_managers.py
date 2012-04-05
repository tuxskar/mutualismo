from operator import attrgetter

from django.contrib.auth.models import User
from django.test import TestCase

from ..managers import TradeManager

class TradeManagerTest(TestCase):
    """Test case for ``TradeManager``."""
    fixtures = ['test.json']

    def setUp(self):
        self.manager = TradeManager()

    # `latest_offers`
    def test_latest_offers_count(self):
        count = 10
        latest_ten_offers = self.manager.latest_offers(count)
        self.assertLessEqual(len(latest_ten_offers), count)

    def test_latest_offer_count_when_negative(self):
        count = -3
        latest_offers = self.manager.latest_offers(count)
        self.assertEqual(0, len(latest_offers))

    def test_latest_offers_sorted_by_date(self):
        latest_offers = self.manager.latest_offers()
        self.assertEqual(latest_offers, sorted(latest_offers, 
                                               key=attrgetter('date'),
                                               reverse=True))


    # `latest_demands`
    def test_latest_demands_count(self):
        count = 10
        latest_ten_demands = self.manager.latest_demands(count)
        self.assertLessEqual(len(latest_ten_demands), count)

    def test_latest_demand_count_when_negative(self):
        count = -3
        latest_demands = self.manager.latest_demands(count)
        self.assertEqual(0, len(latest_demands))

    def test_latest_demands_sorted_by_date(self):
        latest_offers = self.manager.latest_offers()
        self.assertEqual(latest_offers, sorted(latest_offers, 
                                               key=attrgetter('date'),
                                               reverse=True))

    # `offers`
    def test_user_offers(self):
        alice = User.objects.get(username=u'Alice')
        offers = self.manager.offers(alice)
        for offer in offers:
            self.assertEqual(offer.owner, alice)

    def test_user_offers_sorted_by_date(self):
        # newest comes first
        alice = User.objects.get(username=u'Alice')
        offers = self.manager.offers(alice)
        sorted_offers = sorted(list(offers),
                               key=lambda offer: offer.date,
                               reverse=True)
        for index, offer in enumerate(sorted_offers):
            self.assertEqual(offer, offers[index])

    # `demands`
    def test_user_demands(self):
        alice = User.objects.get(username=u'Alice')
        demands = self.manager.demands(alice)
        for demand in demands:
            self.assertEqual(demand.owner, alice)

    def test_user_demands_sorted_by_date(self):
        # newest comes first
        alice = User.objects.get(username=u'Alice')
        demands = self.manager.demands(alice)
        sorted_demands = sorted(list(demands),
                               key=lambda demand: demand.date,
                               reverse=True)
        for index, demand in enumerate(sorted_demands):
            self.assertEqual(demand, demands[index])

    # `services`
    def test_user_services(self):
        alice = User.objects.get(username=u'Alice')
        services = self.manager.services(alice)
        for service in services:
            self.assertEqual(service.owner, alice)

    def test_user_services_sorted_by_date(self):
        # newest comes first
        alice = User.objects.get(username=u'Alice')
        services = self.manager.services(alice)
        sorted_services = sorted(list(services),
                               key=lambda service: service.date,
                               reverse=True)
        for index, service in enumerate(sorted_services):
            self.assertEqual(service, services[index])

    # `gifts`
    def test_user_gifts(self):
        alice = User.objects.get(username=u'Alice')
        gifts = self.manager.gifts(alice)
        for gift in gifts:
            self.assertEqual(gift.owner, alice)

    def test_user_gifts_sorted_by_date(self):
        # newest comes first
        alice = User.objects.get(username=u'Alice')
        gifts = self.manager.gifts(alice)
        sorted_gifts = sorted(list(gifts),
                               key=lambda gift: gift.date,
                               reverse=True)
        for index, gift in enumerate(sorted_gifts):
            self.assertEqual(gift, gifts[index])

    # `loans`
    def test_user_loans(self):
        alice = User.objects.get(username=u'Alice')
        loans = self.manager.loans(alice)
        for loan in loans:
            self.assertEqual(loan.owner, alice)

    def test_user_loans_sorted_by_date(self):
        # newest comes first
        alice = User.objects.get(username=u'Alice')
        loans = self.manager.loans(alice)
        sorted_loans = sorted(list(loans),
                               key=lambda loan: loan.date,
                               reverse=True)
        for index, loan in enumerate(sorted_loans):
            self.assertEqual(loan, loans[index])
