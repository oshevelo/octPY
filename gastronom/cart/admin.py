from django.contrib import admin
from .models import Cart, CartItem


class CartItemAdmin(admin.StackedInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin]
    list_display = ('id', 'user', 'creation_date')
    extra = 1


admin.site.register(Cart, CartAdmin)
