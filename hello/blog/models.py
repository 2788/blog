from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=150)
    create_date = models.DateTimeField(auto_now_add=True)
    modiify_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_show = models.BooleanField()

    class Meta:
        db_table = 'article'

    def __str__(self):
        return self.title

class MyUser(AbstractUser):

    class Meta:
        db_table = 'myuser'

    def __str__(self):
        return self.username

class Comment(models.Model):
    article_id = models.IntegerField()
    username = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.username
