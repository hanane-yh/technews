from rest_framework import serializers
from news.models import News
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['label']


class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'source', 'tags']
