from itertools import chain

from django.db.models import Manager
from django.contrib.auth.models import User

from .models import Offer, Demand, Gift, Loan, Service

class TradeManager(Manager):
    def latest_offers(self, count=None):
        """
        Returns the latest ``count`` offers ordered reversely by date.

        By default it returns all the offers.
        """
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
        Returns the latest ``count`` demands ordered reversely by date.

        By default it returns all the demands.
        """
        latest = Demand.objects.all().order_by('-date')
        if count is None:
            return latest
        elif count > 0:
            return latest[:count]
        else:
            return []

    def offers(self, username, count=None):
        """
        Returns the latest ``count`` offers for the given ``username``
        ordered reversely by date.

        By default it returns all the offers.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Offer.objects.none()

        #offers = Offer.objects.filter(owner=user).order_by('-date')
        loans = Loan.objects.filter(owner=user).order_by('-date')
        gifts = Gift.objects.filter(owner=user).order_by('-date')
        services = Service.objects.filter(owner=user).order_by('-date')
        offers = sorted(chain(loans, gifts, services),
                        key=lambda trade: trade.date,
                        reverse=True)
        if count is None:
            return offers
        elif count > 0:
            return offers[:count]
        else:
            return Offer.objects.none()

    def demands(self, username, count=None):
        """
        Returns the latest ``count`` demands for the given ``username``
        ordered reversely by date.

        By default it returns all the demands.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Demand.objects.none()

        demands = Demand.objects.filter(owner=user).order_by('-date')
        if count is None:
            return demands
        elif count > 0:
            return demands[:count]
        else:
            return Demand.objects.none()

    def services(self, username, count=None):
        """
        Returns the latest ``count`` services owned by the given ``username``.

        By default it returns all the services.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Service.objects.none()

        services = Service.objects.filter(owner=user).order_by('-date')
        if count is None:
            return services
        elif count > 0:
            return services[:count]
        else:
            return Service.objects.none()

    def gifts(self, username, count=None):
        """
        Returns the latest ``count`` gifts owned by the given ``username``.

        By default it returns all the gifts.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Gift.objects.none()

        gifts = Gift.objects.filter(owner=user).order_by('-date')
        if count is None:
            return gifts
        elif count > 0:
            return gifts[:count]
        else:
            return Gift.objects.none()

    def loans(self, username, count=None):
        """
        Returns the latest ``count`` loans owned by the given ``username``.

        By default it returns all the loans.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Loan.objects.none()

        loans = Loan.objects.filter(owner=user).order_by('-date')
        if count is None:
            return loans
        elif count > 0:
            return loans[:count]
        else:
            return Loan.objects.none()

    def total_users(self):
        """
        Return the total of trades
        """
        return User.objects.all().count()

    def total_offers(self):
        """
        Return the total of offers
        """
        return Loan.objects.all().count() \
				+ Gift.objects.all().count() \
				+ Service.objects.all().count()


