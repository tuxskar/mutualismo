from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import ServiceForm
from ..models import Service

class TestServiceForm(TestCase):
    """Test ``ServiceForm`` class."""
    fixtures = ['test.json']

    # FIXME: does not validate even providing just ``name``, ``description`` and
    #        ``owner`` parameters.
    #def test_accepts_datetime_format(self):
        #"""
        #Check that the form accepts datetime in the following format: 
            #'%m/%d/%Y %H:%M'.
        #"""
        #user = User.objects.get(pk=2)
        #service = Service(name='A Test', 
                          #description='test', 
                          #owner=user,)
                          ## ``starts`` and ``ends`` are the fields
                          ## that we are checking
                          ##starts='02/23/2012 14:32',
                          ##ends='02/24/2012 14:49',)
        #service_form = ServiceForm(instance=service)
        #self.assertTrue(service_form.is_valid())
