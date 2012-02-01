from django.shortcuts import render_to_response

from red.managers import TradeManager

def index(request):
    """Index page."""
    trades = TradeManager()
    latest_trades = trades.latest()
    data = {'trades': latest_trades,}
    return render_to_response('index.html', data)

def about(request):
    """About page."""
    return render_to_response('about.html',)
