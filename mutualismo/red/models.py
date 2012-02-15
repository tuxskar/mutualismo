import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager


class Trade(models.Model):
    """
    Represents an object or action which can be part of a trade within our network. 
    """
    name        = models.CharField(_('name'), max_length=124, unique=True)
    description = models.TextField(_('description'))
    date        = models.DateTimeField(_('date'), default = datetime.datetime.now)
    owner       = models.ForeignKey(User)
    tags        = TaggableManager(blank=True)
    # TODO: categorize trades with a 3rd party app
    visible = models.BooleanField(_('visible'), default=True)

    slug        = AutoSlugField(populate_from=('name',), unique=True, max_length=255)
    objects     = models.Manager()

    class Meta:
        abstract = True
        
    def __unicode__(self):
        return u'%s' % self.name


class Offer(Trade):
    """
    Represents a trade that is offered by its owner.
    """
    # This class is convenient because it allows us to have a 
    # foreign key to an ``Offer`` model and use that field with
    # subclasses of ``Offer``.
    @models.permalink
    def get_absolute_url(self):
        return ('red.views.offer', (), {'offer_slug': self.slug})


class Demand(Trade):
    # XXX very provisional.
    TYPE_CHOICE = (
        (0, _('All')),
        (1, _('Service')),
        (2, _('Good for loan')),
        (3, _('Good for gift')),
        (4, _('Communal good')),
    )
    trade_type = models.IntegerField(_('type'), choices = TYPE_CHOICE, default = 0)

    @models.permalink
    def get_absolute_url(self):
        return ('red.views.demand', (), {'demand_slug': self.slug})


class Loan(Offer):
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


class Gift(Offer):
    """
    Represents a good that is gifted by its owner.
    """
    # XXX A gift can pass from non-communal to communal, but not the other way!
    communal  = models.BooleanField(_('communal'))
    available = models.BooleanField(_('available'))

    class Meta:
        verbose_name = _('gift')
        verbose_name_plural = _('gifts')


class Service(Offer):
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
    starts       = models.DateTimeField(_('start date'), blank=True, null=True)
    ends         = models.DateTimeField(_('end date'), blank=True, null=True)
    availability = models.TextField(_('availability'), blank=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')


class Exchange(models.Model):
    """
    Represents an exchange between users.
    """
    # XXX We can discard the `from_user` field since that the `trade` field
    #     contains a reference to its owner.
    #from_user = models.ForeignKey(User, related_name = 'from')
    trade = models.ForeignKey(Offer)
    to    = models.ForeignKey(User, related_name = 'to')
    date  = models.DateTimeField(_('date'), default = datetime.datetime.now)

    class Meta:
        verbose_name = _('exchange')
        verbose_name_plural = _('exchanges')

    def __unicode__(self):
        # TODO
        return u'exchange'
