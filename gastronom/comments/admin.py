from django.contrib import admin
from .models import Review, GalleryImageReview
# Register your models here.


class GalleryImageReviewInline(admin.TabularInline):
    model = GalleryImageReview
    extra = 1


class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'text']}),
    ]
    inlines = [GalleryImageReviewInline]
    list_filter = ['created']
    search_fields = ['user', 'text']


admin.site.register(Review, ReviewAdmin)
admin.site.register(GalleryImageReview)
