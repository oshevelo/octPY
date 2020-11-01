from django.contrib import admin

from .models import Question, Choice



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    pass
    inlines = [ChoiceInline]
    #list_display = ('question_text', 'pub_date', 'question_description', 'was_published_recently')
    #list_filter = ['pub_date']
    #search_fields = ['question_text', 'question_description']
    #date_hierarchy = 'pub_date'
    #fields = [ 'pub_date', 'question_text', 'question_description']

admin.site.register(Question, QuestionAdmin)


admin.site.register(Choice)
