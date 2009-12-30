
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=64)
    date = models.DateField()
    
    def __unicode__(self):
        return self.title