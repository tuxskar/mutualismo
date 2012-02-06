from django.template import RequestContext
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response

from settings import ADMINS

from red.managers import TradeManager
from red.forms import ContactForm

def index(request):
    """Index page."""
    trades = TradeManager()
    latest_offers = trades.latest_offers()
    latest_demands = trades.latest_demands()
    data = {'latest_offers':  latest_offers,
            'latest_demands': latest_demands,}
    return render_to_response('red/index.html', data)

def about(request):
    """About page."""
    return render_to_response('red/about.html',)

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
            return render_to_response('red/thankyou.html', 
                                      RequestContext(request))
    else:
        form = ContactForm()

    return render_to_response('red/contact.html', 
                              {'form': form,}, 
                              RequestContext(request))

def profile(request):
    """User's profile."""
    pass
