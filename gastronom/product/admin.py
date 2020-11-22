from django.contrib import admin

from .models import Product, Media, Characteristic

class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


class MediaInline(admin.StackedInline):
    model = Media
    extra = 1
    
    
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields' : ['name', 'sku', 'price']}),
        ('Product information', {'fields' : ['descriptions', 'raiting']}),
        ]
    
    inlines = [CharacteristicInline, MediaInline]
    list_display = ('name', 'descriptions', 'sku', 'price', 'raiting')
    list_filter = ['raiting', 'price', 'name']
    search_fields = ['name', 'price', 'sku', 'raiting']
    
    
admin.site.register(Product, ProductAdmin)
