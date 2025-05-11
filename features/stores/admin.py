from django.contrib import admin
from django.db.models import ImageField
from image_uploader_widget.widgets import ImageUploaderWidget

from features.stores import forms, models


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "name", "category", "price", "image")
    list_display_links = ("id", "store", "name", "category", "price", "image")
    search_fields = ("name",)
    list_filter = ("store", "category")
    ordering = ("name",)
    list_per_page = 20
    formfield_overrides = {
        ImageField: {"widget": ImageUploaderWidget},
    }


@admin.register(models.PriceProductHistory)
class PriceProductHistoryAdmin(admin.ModelAdmin):  #
    list_display = ("id", "product", "price", "created_at")
    list_display_links = ("id", "product", "price", "created_at")
    search_fields = ("product__name", "price")
    list_filter = ("created_at", "product__store")
    ordering = ("-created_at",)
    list_per_page = 20
