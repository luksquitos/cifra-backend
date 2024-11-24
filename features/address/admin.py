from django.contrib import admin
# from core.softdelete import SoftDeleteModelAdmin
from features.address import models, forms


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "street",
        "district",
        "city",
        "state",
        "postal_code",
        "number",
    ]
    list_filter = ["state"]
    search_fields = ["street", "district", "city", "postal_code"]
    form = forms.AddressForm
