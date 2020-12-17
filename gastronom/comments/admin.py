from django.contrib import admin
from .models import Review, ReviewImage
# Register your models here.


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 2


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'product', 'created', 'updated', 'reply_to']
    fieldsets = [
        (None,               {'fields': ['user', 'product', 'text', 'reply_to']}),
    ]
    inlines = [ReviewImageInline]
    list_filter = ['created']
    search_fields = ['user', 'text', 'product']


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage)
