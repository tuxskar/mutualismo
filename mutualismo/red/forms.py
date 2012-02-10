from django import forms
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    """Form for submitting a message to the site administrators."""
    subject = forms.CharField(label=_("Subject"), max_length=100)
    message = forms.CharField(label=_("Message"))
    sender = forms.EmailField(label=_("Sender"))
    cc_myself = forms.BooleanField(label=_("Send me a copy"), required=False)
