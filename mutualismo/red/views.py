from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404

from settings import ADMINS

from red.managers import TradeManager
from red.models import Offer, Demand, Service, Gift, Loan
from red.forms import ContactForm, DemandForm, ServiceForm, GiftForm, LoanForm


def index(request):
    """Index page."""
    trades = TradeManager()
    latest_offers = trades.latest_offers()
    latest_demands = trades.latest_demands()
    data = {'latest_offers':  latest_offers,
            'latest_demands': latest_demands, }
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

# Read


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


# Create


@login_required
def _create(request, model, form_model, next_view):
    """
    A page for creating an instance of the given ``model`` with
    using the ``form_model`` form and the ``create_<model-name>``.html
    template.
    
    It re-renders itself whit invalid data, and calls ``next_view``
    when the data is valid.
    """
    user = request.user
    if request.method == 'POST': 
        instance = model(owner=user,)
        instance_form = form_model(request.POST, instance=instance) 
        if instance_form.is_valid(): 
            instance_form.save()
            return next_view(request)
        else:
            form = instance_form
    else:
        form = form_model()
    return render_to_response('create_%s.html' % model.__name__.lower(), 
                              {'form': form,}, 
                              RequestContext(request))


@login_required
def create_demand(request):
    """
    Creates a demand belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    return _create(request, Demand, DemandForm, dashboard)


@login_required
def create_service(request):
    """
    Creates a service offer belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    return _create(request, Service, ServiceForm, dashboard)


@login_required
def create_gift(request):
    """
    Creates a gift offer belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    return _create(request, Gift, GiftForm, dashboard)


@login_required
def create_loan(request):
    """
    Creates a loan offer belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    return _create(request, Loan, LoanForm, dashboard)


# Edit

# TODO
@login_required
def _edit(request, slug):
    pass


@login_required
def edit_demand(request, demand_slug):
    """
    Edits a demand belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_demands = trades.demands(user.username)
    demand = get_object_or_404(user_demands, slug=demand_slug)
    if request.method == 'POST': 
        demand_form = DemandForm(request.POST, instance=demand) 
        if demand_form.is_valid(): 
            demand_form.save()
            return dashboard(request)
        else:
            form = demand_form
    else:
        form = DemandForm(instance=demand)
    return render_to_response('edit_demand.html', 
                              {'form': form,
                               'demand': demand}, 
                              RequestContext(request))


@login_required
def edit_service(request, service_slug):
    """
    Edits a service belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_services = trades.services(user.username)
    service = get_object_or_404(user_services, slug=service_slug)
    if request.method == 'POST': 
        service_form = ServiceForm(request.POST, instance=service) 
        if service_form.is_valid(): 
            service_form.save()
            return dashboard(request)
        else:
            form = service_form
    else:
        form = ServiceForm(instance=service)
    return render_to_response('edit_service.html', 
                              {'form': form,
                               'service': service}, 
                              RequestContext(request))


@login_required
def edit_gift(request, gift_slug):
    """
    Edits a gift belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_gifts = trades.gifts(user.username)
    gift = get_object_or_404(user_gifts, slug=gift_slug)
    if request.method == 'POST': 
        gift_form = GiftForm(request.POST, instance=gift) 
        if gift_form.is_valid(): 
            gift_form.save()
            return dashboard(request)
        else:
            form = gift_form
    else:
        form = GiftForm(instance=gift)
    return render_to_response('edit_gift.html', 
                              {'form': form,
                               'gift': gift}, 
                              RequestContext(request))
    

@login_required
def edit_loan(request, loan_slug):
    """
    Edits a loan belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_loans = trades.loans(user.username)
    loan = get_object_or_404(user_loans, slug=loan_slug)
    if request.method == 'POST': 
        loan_form = LoanForm(request.POST, instance=loan) 
        if loan_form.is_valid(): 
            loan_form.save()
            return dashboard(request)
        else:
            form = loan_form
    else:
        form = LoanForm(instance=loan)
    return render_to_response('edit_loan.html', 
                              {'form': form,
                               'loan': loan}, 
                              RequestContext(request))


# Delete

# TODO
@login_required
def _delete(request, slug):
    pass


@login_required
def delete_demand(request, demand_slug):
    """
    Deletes the demand corresponding to the given slug if it belongs
    to the user who is logged in.

    After that, redirects to the dashboard.
    """
    user = request.user
    username = user.username
    trades = TradeManager()
    user_demands = trades.demands(username)
    demand_to_delete = get_object_or_404(user_demands, slug=demand_slug) 
    if demand_to_delete:
        demand_to_delete.delete()
    return dashboard(request)


@login_required
def delete_offer(request, offer_slug):
    """
    Deletes the offer corresponding to the given slug if it belongs
    to the user who is logged in.

    After that, redirects to the dashboard.
    """
    user = request.user
    username = user.username
    trades = TradeManager()
    user_offers = trades.offers(username)
    offer_to_delete = get_object_or_404(user_offers, slug=offer_slug) 
    if offer_to_delete:
        offer_to_delete.delete()
    return dashboard(request)
