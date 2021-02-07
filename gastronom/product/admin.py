from django.contrib import admin

from .models import Product, ProductMedia, Characteristic

class CharacteristicInline(admin.StackedInline):
    model = Characteristic
    extra = 1

class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1
    
    
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields' : ['categories', 'name', 'sku', 'price', 'productcount', 'descriptions', 'raiting', 'available', ]}),
        ]
    
    inlines = [CharacteristicInline, ProductMediaInline]
    list_display = ('name', 'descriptions', 'sku', 'price', 'raiting', 'productcount', 'available')
    list_filter = ['raiting', 'price', 'name']
    search_fields = ['name', 'price', 'sku', 'raiting']
    list_editable = ['price', 'raiting', 'productcount']
    
    
admin.site.register(Product, ProductAdmin)
