from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response

from settings import ADMINS

from red.managers import TradeManager
from red.models import Offer, Demand
from red.forms import ContactForm
def index(request):
    """Index page."""
    trades = TradeManager()
    latest_offers = trades.latest_offers()
    latest_demands = trades.latest_demands()
    data = {'latest_offers':  latest_offers,
            'latest_demands': latest_demands,}
    return render_to_response('index.html', data)

def about(request):
    """About page."""
    return render_to_response('about.html',)

def contact(request):
    """Contact page."""
    if request.method == 'POST': 
        form = ContactForm(request.POST) 
        if form.is_valid(): 
            # process and send mails
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = []
            for name, email in ADMINS:
                recipients.append(email)

            email = EmailMessage(subject=subject,
                                 from_email=sender,
                                 body=message,
                                 to=recipients,)
            if cc_myself:
                email.cc = [sender]
            email.send()
            return render_to_response('thankyou.html', 
                                      RequestContext(request))
    else:
        form = ContactForm()

    return render_to_response('contact.html', 
                              {'form': form,}, 
                              RequestContext(request))

@login_required
def dashboard(request):
    """User's dashboard page."""
    user = request.user
    username = user.username
    trades = TradeManager()
    offers = trades.offers(username)
    demands = trades.demands(username)
    data = {'username': username,
            'offers':   offers,
            'demands':  demands,}
    return render_to_response('dashboard.html', 
                              data,
                              RequestContext(request))

def _trade(request, cls, slug):
    """
    Helper function to render a certain trade given its class and slug.
    """
    try:
        trade = cls.objects.get(slug=slug)
    except cls.DoesNotExist:
        trade = None
    trade_type = cls.__name__.lower()
    data = {trade_type: trade,}
    return render_to_response('trade.html',
                              data,
                              RequestContext(request))

def offer(request, offer_slug):
    """Shows information about a certain offer."""
    return _trade(request, Offer, offer_slug)

def demand(request, demand_slug):
    """Shows information about a certain demand."""
    return _trade(request, Demand, demand_slug)
