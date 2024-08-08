from django.db import models


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    reading_time = models.PositiveIntegerField()
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
