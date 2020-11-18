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
        (None,                  {'fields' : ['product_name']}),
        ('Product information', {'fields' : ['product_descriptions', 'product_raiting']}),
        ]
    
    inlines = [CharacteristicInline, MediaInline]
    list_display = ('product_name', 'product_descriptions', 'product_raiting')
    list_filter = ['product_raiting']
    search_fields = ['product_name']
    
    
admin.site.register(Product, ProductAdmin)
