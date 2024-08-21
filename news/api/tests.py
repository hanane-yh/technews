from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from news.models import News, Tag
from .serializers import NewsSerializer
from django.shortcuts import get_object_or_404


class NewsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create sample tags
        self.tag1 = Tag.objects.create(label='tag1')
        self.tag2 = Tag.objects.create(label='tag2')

        self.news1 = News.objects.create(
            title='News 1',
            content='Content 1',
            source='Source 1',
            url='http://example.com/news1'
        )
        self.news1.tags.add(self.tag1)

        self.news2 = News.objects.create(
            title='News 2',
            content='Content 2',
            source='Source 2',
            url='http://example.com/news2'
        )
        self.news2.tags.add(self.tag2)

        self.news3 = News.objects.create(
            title='News 3',
            content='Content 3',
            source='Source 3',
            url='http://example.com/news3'
        )
        self.news3.tags.add(self.tag1, self.tag2)

    def test_get_routes(self):
        response = self.client.get(reverse('get-routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            'GET /api',
            'GET /api/news',
            'GET /api/news/:id'
        ])

    def test_list_all_news(self):
        response = self.client.get(reverse('list-news'))
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_news_by_tag(self):
        response = self.client.get(reverse('list-news'), {'tag': 'tag1'})
        news = News.objects.filter(tags__label='tag1')
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(reverse('list-news'), {'tag': 'tag2'})
        news = News.objects.filter(tags__label='tag2')
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_specific_news(self):
        response = self.client.get(reverse('get-news', args=[self.news1.id]))
        news = News.objects.get(id=self.news1.id)
        serializer = NewsSerializer(news)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

        response = self.client.get(reverse('get-news', args=[self.news2.id]))
        news = News.objects.get(id=self.news2.id)
        serializer = NewsSerializer(news)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_news(self):
        response = self.client.get(reverse('get-news', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_news_by_nonexistent_tag(self):
        response = self.client.get(reverse('list-news'), {'tag': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_news_count(self):
        response = self.client.get(reverse('news_count'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'total_news_sscraped': 3})
