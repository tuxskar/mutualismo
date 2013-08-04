from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404

from mutualismo.settings import ADMINS

from registration.forms import RegistrationForm

from .managers import TradeManager
from .models import Demand, Service, Gift, Loan
from .forms import ContactForm, DemandForm, ServiceForm, GiftForm, LoanForm


def index(request):
    """Index page."""
    trades = TradeManager()
    latest_offers = trades.latest_offers()
    latest_demands = trades.latest_demands()
    login_form = AuthenticationForm()
    registration_form = RegistrationForm()
    data = {'latest_offers':     latest_offers,
            'latest_demands':    latest_demands,
            'login_form':        login_form,
            'registration_form': registration_form,}
    return render_to_response('index.html',
                              data,
                              RequestContext(request))


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


def _trade(request, model, slug):
    """
    Helper function to render a certain trade given its class and slug.
    """
    try:
        trade = model.objects.get(slug=slug)
    except model.DoesNotExist:
        trade = None
    data = {'trade': trade,}
    return render_to_response('trade.html',
                              data,
                              RequestContext(request))

def offer(request, offer_slug):
    """Shows information about a certain offer."""
    # XXX Ugly hack (TM)  XXX
    #  The problem here is that if we pass an `Offer` object
    #  to the view, we are not able to determine its subclass
    #  and render the proper template.
    for cls in [Service, Gift, Loan]:
        try:
            cls.objects.get(slug=offer_slug)
        except cls.DoesNotExist:
            continue
        else:
            return _trade(request, cls, offer_slug)

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
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
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


def _edit(request, model, form_model, user_instances, slug, next_view):
    """
    Given a ``model``, a form for editing that model ``form_model``, the
    ``user_instances`` of that model and the ``slug`` of one of them, renders
    a view in which that instance, if exists, can be modified and saved.

    If the instance is not found, a 404 error is raised. Otherwise, the
    modified instance is saved and ``next_view`` is called with the ``request``
    parameter.
    """
    instance = get_object_or_404(user_instances, slug=slug)
    if request.method == 'POST':
        instance_form = form_model(request.POST, instance=instance)
        if instance_form.is_valid():
            instance_form.save()
            return next_view(request)
        else:
            form = instance_form
    else:
        form = form_model(instance=instance)
    model_name = model.__name__.lower()
    return render_to_response('edit_%s.html' % (model_name),
                              {'form': form,
                               model_name: instance},
                               RequestContext(request))


@login_required
def edit_demand(request, demand_slug):
    """
    Edits a demand belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_demands = trades.demands(user.username)
    return _edit(request=request,
                 model=Demand,
                 form_model=DemandForm,
                 user_instances=user_demands,
                 slug=demand_slug,
                 next_view=dashboard)


@login_required
def edit_service(request, service_slug):
    """
    Edits a service belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_services = trades.services(user.username)
    return _edit(request=request,
                 model=Service,
                 form_model=ServiceForm,
                 user_instances=user_services,
                 slug=service_slug,
                 next_view=dashboard)


@login_required
def edit_gift(request, gift_slug):
    """
    Edits a gift belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_gifts = trades.gifts(user.username)
    return _edit(request=request,
                 model=Gift,
                 form_model=GiftForm,
                 user_instances=user_gifts,
                 slug=gift_slug,
                 next_view=dashboard)


@login_required
def edit_loan(request, loan_slug):
    """
    Edits a loan belonging to the logged in user.

    After that, redirects to the dashboard.
    """
    user = request.user
    trades = TradeManager()
    user_loans = trades.loans(user.username)
    return _edit(request=request,
                 model=Loan,
                 form_model=LoanForm,
                 user_instances=user_loans,
                 slug=loan_slug,
                 next_view=dashboard)


# Delete

def _delete(request, user_instances, slug, next_view):
    """
    Deletes the instance of corresponding to the given slug
    if its in ``user_instances``.

    After that, renders ``next_view``.
    """
    instance_to_delete = get_object_or_404(user_instances, slug=slug)
    if instance_to_delete:
        instance_to_delete.delete()
    return next_view(request)


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
    return _delete(request=request,
                   user_instances=user_demands,
                   slug=demand_slug,
                   next_view=dashboard)


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
    return _delete(request=request,
                   user_instances=user_offers,
                   slug=offer_slug,
                   next_view=dashboard)
