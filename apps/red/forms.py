from django.forms import Form, ModelForm, CharField, EmailField, BooleanField
from django.utils.translation import ugettext_lazy as _

from .models import Demand, Service, Gift, Loan


class ContactForm(Form):
    """Form for submitting a message to the site administrators."""
    subject = CharField(label=_("Subject"), max_length=100)
    message = CharField(label=_("Message"))
    sender = EmailField(label=_("Sender"))
    cc_myself = BooleanField(label=_("Send me a copy"), required=False)


class DemandForm(ModelForm):
    """Form for creating or modifying a demand."""
    class Meta:
        model = Demand
        fields = ('name', 'description', 'trade_type', 'tags',)


class ServiceForm(ModelForm):
    """Form for creating or modifying a service as an offer."""
    class Meta:
        model = Service
        # TODO: ``starts`` and ``ends`` fields with validation
        fields = ('name', 'description', 'availability', 'tags',)


class GiftForm(ModelForm):
    """Form for creating or modifying a gift as an offer."""
    class Meta:
        model = Gift
        fields = ('name', 'description', 'available', 'communal', 'tags',)


class LoanForm(ModelForm):
    """Form for creating or modifying a loan as an offer."""
    class Meta:
        model = Loan
        fields = ('name', 'description', 'status', 'tags',)
