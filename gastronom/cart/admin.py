from django.contrib import admin
from .models import Cart, CartItem


class CartItemAdmin(admin.StackedInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin]
    list_display = ('id', 'user', 'creation_date')


admin.site.register(Cart, CartAdmin)


# class CartInLine(admin.TabularInline):
#     model = Cart
#     extra = 1
#
#
# admin.site.register(Cart)
