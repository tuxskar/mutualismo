from django.contrib.auth.models import User as BaseUser
from django.db import models


class Category(models.Model):
    name        = models.CharField(max_length=124)
    description = models.TextField()

class SubCategory(Category):
    parent = models.ForeignKey(Category, related_name='sub')


class Trade(models.Model):
    """
    Represents an object or action which can be part of a trade within our network. 
    """
    name        = models.CharField(max_length=124)
    description = models.TextField()
    category    = models.ForeignKey(Category)
    # TODO tags


class Good(Trade):
    """
    Represents a good that can be offered or demanded. 
    """
    # XXX should be mandatory for offers, N/A for demands
    #STATE = ('')
    pass


class Loan(Good):
    """
    Represents a good that is available for loan.
    """
    # TODO we are discussing this
    max_time = models.CharField(max_length=140)


class Gift(Good):
    """
    Represents a good that is gifted by his/her owner.
    """
    communal = models.BooleanField()


class Service(Trade):
    """
    Represents a service that can be offered or demanded.  
    """
    starts       = models.DateTimeField()
    ends         = models.DateTimeField()
    availability = models.TextField()


class Exchange(models.Model):
    """
    Represents an exchange between two users.
    """
    #CHOICE (give, receive)
    trade    = models.ForeignKey(Trade)
    date     = models.DateTimeField()


class User(BaseUser):
    """
    Extends the ``django.contrib.auth.User`` class to store offers, demands, a
    history of the exchanges and more suitable information.
    """
    offerings = models.ManyToManyField(Trade, related_name='offer')
    demands   = models.ManyToManyField(Trade, related_name='demand')
    history   = models.ManyToManyField(Exchange)
    location  = models.CharField(max_length=124)
