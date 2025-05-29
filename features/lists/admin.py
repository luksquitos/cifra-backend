from django.contrib import admin

from core.admin import site
from features.lists import models


class ProductInline(admin.TabularInline):
    model = models.ProductList
    extra = 0
    readonly_fields = ["price", "total_price"]


@admin.register(models.UserList, site=site)
class ListsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "total_price", "best_store", "last_update"]
    list_display_links = [
        "id",
        "user",
        "name",
        "total_price",
        "best_store",
        "last_update",
    ]
    list_filter = ["user", "last_update"]
    inlines = [ProductInline]
    readonly_fields = ["best_store", "last_update", "total_price"]
