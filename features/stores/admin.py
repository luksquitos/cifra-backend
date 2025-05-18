from django.contrib import admin

from features.stores import models


class ProductHistoryInline(admin.TabularInline):
    model = models.PriceProductHistory
    extra = 0
    classes = ("collapse",)
    readonly_fields = ("created_at", "price")
    
    def has_add_permission(self, request, obj):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False

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
    inlines = [ProductHistoryInline]
    list_per_page = 20


@admin.register(models.PriceProductHistory)
class PriceProductHistoryAdmin(admin.ModelAdmin):
    # Pode ser deletado depois de ter integração com lojistas
    list_display = ("id", "product", "price", "created_at")
    list_display_links = ("id", "product", "price", "created_at")
    search_fields = ("product__name", "price")
    list_filter = ("created_at", "product__store")
    ordering = ("-created_at",)
    list_per_page = 20