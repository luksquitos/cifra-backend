from django.contrib import admin
from django.db.models import ImageField
from image_uploader_widget.widgets import ImageUploaderWidget

from core.admin import site
from features.stores import models


class SpecificCharacteristicInline(admin.TabularInline):
    model = models.ProductTechnicalCharacteristics
    classes = ("collapse",)
    extra = 0


class ProductHistoryInline(admin.TabularInline):
    model = models.PriceProductHistory
    extra = 0
    classes = ("collapse",)
    readonly_fields = ("created_at", "price")
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=...):
        return False


@admin.register(models.Store, site=site)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(models.ProductTechnicalCharacteristics, site=site)
class ProductTechnicalCharacteristicsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category, site=site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(models.Product, site=site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "name", "category", "price", "image")
    search_fields = ("name",)
    list_filter = ("store", "category")
    ordering = ("name",)
    inlines = [ProductHistoryInline]
    list_per_page = 20
    inlines = [SpecificCharacteristicInline, ProductHistoryInline]
    formfield_overrides = {
        ImageField: {"widget": ImageUploaderWidget},
    }

    def get_fields(self, request, obj=...):
        fields = list(super().get_fields(request, obj))
        if not request.user.is_superuser:
            fields.remove("store")

        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.store = request.user.store
        obj.save()

    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        return ("name", "category", "price", "image")

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ("category",)

    def get_list_display_links(self, request, list_display):
        return self.list_display

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        store = models.Store.objects.get(user=request.user)
        return models.Product.objects.select_related("store").filter(store=store)

    class Media:
        js = ("js/admin_no_multiple_clicks.js",)


@admin.register(models.PriceProductHistory, site=site)
class PriceProductHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price", "created_at")
    list_display_links = ("id", "product", "price", "created_at")
    search_fields = ("product__name", "price")
    list_filter = ("created_at", "product__store")
    ordering = ("-created_at",)
    list_per_page = 20
