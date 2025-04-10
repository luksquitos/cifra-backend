from django.contrib import admin

from features.stores import models


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

    def store_name(self, obj):
        return obj.store.name

    store_name.admin_order_field = "store"
    store_name.short_description = "Nome da Loja"

    def category_name(self, obj):
        return obj.category.name

    category_name.admin_order_field = "category"
    category_name.short_description = "Categoria"


@admin.register(models.PriceProductHistory)
class PriceProductHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price", "created_at")
    list_display_links = ("id", "product", "price", "created_at")
    search_fields = ("product__name", "price")
    list_filter = ("created_at", "product__store")
    ordering = ("-created_at",)
    list_per_page = 20

    def product_name(self, obj):
        return obj.product.name

    product_name.admin_order_field = "product"
    product_name.short_description = "Produto"

    def store_name(self, obj):
        return obj.product.store.name

    store_name.admin_order_field = "product__store"
    store_name.short_description = "Loja do Produto"
