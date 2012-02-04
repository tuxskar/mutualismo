from django.core.mail import EmailMessage
from django.views.generic.simple import direct_to_template
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
            return direct_to_template(request, 'thankyou.html')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {'form': form,})
