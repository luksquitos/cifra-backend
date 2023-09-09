from django.contrib import admin
from .models import Market, Product, ProductImage

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]    
