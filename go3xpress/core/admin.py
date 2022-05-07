from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from go3xpress.utils.export_as_csv import ExportCsvMixin
from .models import Currency, Delivery, DeliveryHistory, Privacy


admin.site.register(Privacy)
admin.site.register(DeliveryHistory)
class CurrencyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('code', 'symbol', 'price', 'created', 'modified')
    list_filter = ('created', 'modified')
    search_fields = ('code', 'symbol', 'price')

    actions = [
        "export_as_csv",
    ]

    # def save_model(self, request, obj, form, change):
    #     user = request.user
    #     if change and form.is_valid():
    #         obj.admin = user
    #         obj.save()
    #     super().save_model(request, obj, form, change)


admin.site.register(Currency, TranslatableAdmin)

class DeliveryAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Delivery
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = [
        '__str__',
        "item_name",
        "last_loc",
        "cost",
        # "variation_active",
        "delivered",
    ]
    list_display_links = ['__str__']
    list_editable = [
        "last_loc",
        "delivered",
        'cost'
    ]
    actions = [
        "export_as_csv",
    ]

admin.site.register(Delivery, DeliveryAdmin)
