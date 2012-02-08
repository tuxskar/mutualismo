from itertools import chain

from django.db.models import Manager
from django.contrib.auth.models import User

from red.models import Offer, Demand, Gift, Loan, Service

class TradeManager(Manager):
    def latest_offers(self, count=20):
        """Returns the latest ``count`` offers ordered by date."""
        # TODO use ``latest``
        loans = Loan.objects.all()
        gifts = Gift.objects.all()
        services = Service.objects.all()
        latest = sorted(chain(loans, gifts, services), 
                        key=lambda trade: trade.date,
                        reverse=True)
        if count < 0:
            count = 0
        return latest[:count]

    def latest_demands(self, count=20):
        """Returns the latest ``count`` demands ordered by date."""
        # TODO ordered by date: ``latest``
        if count < 0:
            count = 0
        return Demand.objects.all()[:count]

    def offers(self, username, count=20):
        """Returns the offers for the given ``username``."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Offer.objects.none()
        return Offer.objects.filter(owner=user)

    def demands(self, username, count=20):
        """Returns the demands for the given ``username``."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Demand.objects.none()
        return Demand.objects.filter(owner=user)
