from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=10)
    pub_date = models.DateTimeField('date published')  
    question_votes = models.IntegerField(default=0)
    question_desc = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return '{} {}'.format(self.id, self.question_text)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
