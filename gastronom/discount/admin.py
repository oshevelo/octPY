from django.contrib import admin
from .models import *


@admin.register(DiscountCart)
class DiscountCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DiscountCart._meta.fields]
    search_fields = ['id', 'cart', 'code']

    class Meta:
        model = DiscountCart

