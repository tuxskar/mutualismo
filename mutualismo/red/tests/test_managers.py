from operator import attrgetter

from django.test import TestCase

from red.managers import TradeManager

class TradeManagerTest(TestCase):
    """Test case for ``TradeManager``."""
    fixtures = ['test.json']

    def setUp(self):
        self.manager = TradeManager()
    
    def test_latest_count(self):
        count = 10
        latest_ten_trades = self.manager.latest(count)
        self.assertLessEqual(count, len(latest_ten_trades))

    def test_latest_count_when_negative(self):
        count = -3
        latest = self.manager.latest(count)
        self.assertEqual(0, len(latest))

    def test_latest_sorted_by_date(self, urls):
        latest_trades = self.manager.latest()
        self.assertEqual(latest_trades, sorted(latest_trades, 
                                               key=attrgetter('date'),
                                               reverse=True))
