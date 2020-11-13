from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    descriptions = models.CharField(max_length=500)
    raiting = models.DecimalField(max_digits=3, decimal_places=1)
    
    def __str__(self):
        return self.name


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mediafiles')
    photo = models.ImageField(blank=True)
    

class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic = models.CharField(max_length=20)
    descriptions = models.CharField(max_length=500)
    
    def __str__(self):
        return self.characteristic

    
class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    # user = models.ForeignKey(User)
    raiting = models.DecimalField(max_digits=3, decimal_places=1)
    feedback_text = models.CharField(max_length=500)
    advantuges = models.CharField(max_length=200)
    disadvantuges = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.feedback_text


class Question(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    # user = models.ForeignKey(User)
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_text
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    # user = models.ForeignKey(User)
    answer_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.answer_text
    
