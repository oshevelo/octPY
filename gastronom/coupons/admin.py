from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_till', 'discount_value', 'description', 'active', 'created_at', 'updated_at']
    list_filter = ['active', 'valid_from', 'valid_till']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)

