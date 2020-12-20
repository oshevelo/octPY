from django.db import models
from tinymce.models import HTMLField


class InfoPost(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    index = models.IntegerField(default=1, primary_key=True)

    def __str__(self):
        return self.title
