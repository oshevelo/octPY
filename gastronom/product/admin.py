from django.contrib import admin

from .models import Product, ProductMedia, Characteristic

class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1

class ProductMediaInline(admin.StackedInline):
    model = ProductMedia
    extra = 1
    
    
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields' : ['categories', 'name', 'sku', 'price', 'count', 'available']}),
        ('Product information', {'fields' : ['descriptions', 'raiting']}),
        ]
    
    inlines = [CharacteristicInline, ProductMediaInline]
    list_display = ('name', 'descriptions', 'sku', 'price', 'raiting', 'count', 'available')
    list_filter = ['raiting', 'price', 'name']
    search_fields = ['name', 'price', 'sku', 'raiting']
    list_editable = ['price', 'raiting', 'count']
    
    
admin.site.register(Product, ProductAdmin)
