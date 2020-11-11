from django.contrib import admin
from .models import Reviews, CommentGalleryItem
# Register your models here.


class CommentGalleryItemInline(admin.TabularInline):
    model = CommentGalleryItem
    extra = 1


class ReviewsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'text']}),
    ]
    inlines = [CommentGalleryItemInline]
    # list_display = ('question_text', 'pub_date', 'question_description', 'was_published_recently')
    list_filter = ['created']
    search_fields = ['user', 'text']


admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(CommentGalleryItem)
