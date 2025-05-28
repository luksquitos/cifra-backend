from django.contrib import admin

from core.admin import site
from features.lists import models


class ProductInline(admin.TabularInline):
    model = models.ProductList
    extra = 0


@admin.register(models.UserList, site=site)
class ListsAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
