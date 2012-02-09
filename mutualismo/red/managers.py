from itertools import chain

from django.db.models import Manager
from django.contrib.auth.models import User

from red.models import Offer, Demand, Gift, Loan, Service

class TradeManager(Manager):
    def latest_offers(self, count=None):
        """
        Returns the latest ``count`` offers ordered by date.
        
        By default it returns all the offers.
        """
        # TODO use ``latest``
        loans = Loan.objects.all()
        gifts = Gift.objects.all()
        services = Service.objects.all()
        latest = sorted(chain(loans, gifts, services), 
                        key=lambda trade: trade.date,
                        reverse=True)

        if count is None:
            return latest
        elif count > 0: 
            return latest[:count]
        else: 
            return []

    def latest_demands(self, count=None):
        """
        Returns the latest ``count`` demands ordered by date.
        
        By default it returns all the demands.
        """
        # TODO ordered by date: ``latest``
        latest = Demand.objects.all()
        if count is None:
            return latest
        elif count > 0: 
            return latest[:count]
        else: 
            return []

    def offers(self, username, count=None):
        """
        Returns the latest ``count`` offers for the given ``username``.
        
        By default it returns all the offers.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Offer.objects.none()

        offers = Offer.objects.filter(owner=user)
        if count is None:
            return offers
        elif count > 0: 
            return offers[:count]
        else:
            return Offer.objects.none()

    def demands(self, username, count=None):
        """
        Returns the latest ``count`` demands for the given ``username``.
        
        By default it returns all the demands.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Demand.objects.none()

        demands = Demand.objects.filter(owner=user)
        if count is None:
            return demands
        elif count > 0: 
            return demands[:count]
        else:
            return Demand.objects.none()
