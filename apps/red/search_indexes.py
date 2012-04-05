from datetime import datetime

from haystack import indexes

from .models import Demand, Service, Gift, Loan


class DemandIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')
    owner = indexes.CharField(model_attr='owner')
    
    def get_model(self):
        return Demand

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(visible=True)

    
class ServiceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')
    owner = indexes.CharField(model_attr='owner')
    
    def get_model(self):
        return Service

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(ends__gt=datetime.now()).filter(visible=True)


class GiftIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')
    owner = indexes.CharField(model_attr='owner')
    
    def get_model(self):
        return Gift

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(available=True).filter(visible=True)


class LoanIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date = indexes.DateTimeField(model_attr='date')
    owner = indexes.CharField(model_attr='owner')
    
    def get_model(self):
        return Loan

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status=1).filter(visible=True)
