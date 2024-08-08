from rest_framework import serializers
from news.models import News
from django.db import models


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'tags']
