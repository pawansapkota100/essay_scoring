from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    """ A model of the 8 questions. """
    question_title = models.TextField(max_length=100000)
    set = models.IntegerField(unique=True)
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return str(self.set)

class Essay(models.Model):
    """ Essay to be submitted. """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=100000)
    score = models.IntegerField(null=True, blank=True)
from django.utils import timezone
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

class Tag(models.Model):
    name = models.CharField(max_length=50)
class Form_Question(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    expectation = models.CharField(max_length=255)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    votes = models.IntegerField(default=0)
    Comment= models.ManyToManyField(Comment, null=True, blank=True, related_name='comments')


