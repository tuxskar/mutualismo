from itertools import chain

from django.db.models import Manager

from red.models import Trade, Gift, Loan, Service

class TradeManager(Manager):
    def latest(self, count=20):
        """Returns the latest ``count`` trades ordered by date."""
        loans = Loan.objects.all()
        gifts = Gift.objects.all()
        services = Service.objects.all()
        latest = sorted(chain(loans, gifts, services), 
                        key=lambda trade: trade.date,
                        reverse=True)
        if count < 0:
            count = 0
        return latest[:count]
