import datetime

from django.contrib.auth.models import User as BaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager


class Category(models.Model):
    name        = models.CharField(_('name'), max_length=124)
    description = models.TextField(_('description'))
    slug        = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name        = _('category')
        verbose_name_plural = _('categories')
        ordering            = ('name',)

    def __unicode__(self):
        return u'%s' % self.name


class SubCategory(Category):
    parent = models.ForeignKey(Category, related_name='sub')


class Trade(models.Model):
    """
    Represents an object or action which can be part of a trade within our network. 
    """
    name        = models.CharField(_('name'), max_length=124)
    description = models.TextField(_('description'))
    # XXX Are we going to allow uncategorized trades? 
    category    = models.ForeignKey(Category)
    # XXX For implementing the one (User) to many (Trade) relationship maybe we
    #     should include a field with a Foreign Key to User instead of having
    #     ManyToManyFields from User to Trade.
    owner       = models.ForeignKey(BaseUser)
    tags        = TaggableManager()

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s' % self.name


class TradeOffer(Trade):
    """
    Represents a trade that is offered by its owner.
    """
    # XXX Maybe we should include a field to control the trade's visibility.
    #     This way, when the user gives it to somebody else or it's no longer
    #     available can be 'erased' changing this field to False.
    visible = models.BooleanField(_('visible'), default=True)


class TradeDemand(Trade):
    # XXX very provisional.
    TYPE_CHOICE = (
        (0, _('All')),
        (1, _('Service')),
        (2, _('Good for loan')),
        (3, _('Good for gift')),
        (4, _('Communal good')),
    )
    trade_type = models.IntegerField(_('type'), choices = TYPE_CHOICE, default = 1)
    # TODO field for specifying if the demand is still being required.


class Loan(TradeOffer):
    """
    Represents a good that is available for loan.
    """
    STATUS_CHOICES = (
        (1, _('Available')),
        (2, _('Reserved')),
        (3, _('Not available')),
    )
    status = models.IntegerField(_('status'), choices = STATUS_CHOICES, default = 1)
    # XXX: Are we going to specify time ranges for loans? Could be optional

    class Meta:
        verbose_name = _('loan')
        verbose_name_plural = _('loans')


class Gift(TradeOffer):
    """
    Represents a good that is gifted by its owner.
    """
    # XXX A gift can pass from non-communal to communal, but not the other way!
    communal  = models.BooleanField(_('communal'))
    available = models.BooleanField(_('available'))

    class Meta:
        verbose_name = _('gift')
        verbose_name_plural = _('gifts')


class Service(TradeOffer):
    """
    Represents a service that can be offered or demanded.  
    """
    # XXX This is a bit rudimentary, check the Django fields to find
    #     a range of dates with more granularity. We want to be able to specify
    #     the ranges of hours when the service is available in every single
    #     day. 
    #
    #     If there are not suitable fields for this, check for 3rd party apps
    #     that provide the wanted functionality.
    starts       = models.DateTimeField(_('start date'))
    ends         = models.DateTimeField(_('end date'))
    availability = models.TextField(_('availability'))

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')


class User(BaseUser):
    """
    Extends the ``django.contrib.auth.User`` class to store offers, demands, a
    history of the exchanges and more suitable information.
    """
    # XXX offerings and demands are related to ONE user; the two relations are
    #     are mutually exclusive.
    # XXX avatar, self description, etc.
    offerings = models.ManyToManyField(TradeOffer, related_name='offer')
    demands   = models.ManyToManyField(TradeDemand, related_name='demand')
    location  = models.CharField(max_length=124)


class Exchange(models.Model):
    """
    Represents an exchange between users.
    """
    # XXX We can discard the `from_user` field since that the `trade` field
    #     contains a reference to its owner.
    #from_user = models.ForeignKey(User, related_name = 'from')
    trade = models.ForeignKey(TradeOffer)
    to    = models.ForeignKey(User, related_name = 'to')
    date  = models.DateTimeField(_('date'), default = datetime.datetime.now)

    class Meta:
        verbose_name = _('exchange')
        verbose_name_plural = _('exchanges')

    def __unicode__(self):
        # TODO
        return u'exchange'
