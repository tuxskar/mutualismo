from django.contrib import admin
from red.models import Loan, Gift, Service, Demand, Exchange

class LoanAdmin(admin.ModelAdmin):
    pass


class GiftAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    pass


class DemandAdmin(admin.ModelAdmin):
    pass


class ExchangeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Loan, LoanAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(Exchange, ExchangeAdmin)
