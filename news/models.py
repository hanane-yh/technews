from django.db import models
from tags.models import Tag

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    source = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(Tag, related_name='news')
    url = models.URLField(unique=True)
    # created_at = models.DateTimeField(auto_now=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title