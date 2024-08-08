from django.db import models
from tags.models import Tag

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, related_name='news')
    # created_at = models.DateTimeField(auto_now=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title