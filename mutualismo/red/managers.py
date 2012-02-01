from django.db.models import Manager

from red.models import Trade, Gift, Loan, Service

class TradeManager(Manager):
    # TODO
    def all(self):
        """Returns all the trades ordered by date."""
        loans = list(Loan.objects.all())
        gifts = list(Gift.objects.all())
        services = list(Service.objects.all())
        trades = [loans, gifts, services]
        all_trades = []
        for trade in trades:
            all_trades.extend(trade)
        return all_trades
