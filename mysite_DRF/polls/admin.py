from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Do you want to publish', {'fields': ['status']}),
        ('Author',               {'fields': ['author']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date','author','was_published_recently','status')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    date_hierarchy = 'pub_date'
    
    def make_published(self, request, queryset):
        queryset.update(status='p')

    make_published.short_description = "Mark selected stories as published"
    actions = 'make_published'

    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)