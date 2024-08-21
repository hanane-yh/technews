from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from news.models import News
from .serializers import NewsSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/news',
        'GET /api/news/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def list_news(request):
    tags = request.query_params.getlist('tag', None)
    if tags:
        news = News.objects.all()
        for tag in tags:
            news = news.filter(tags__label=tag)
    else:
        news = News.objects.all()

    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    serializer = NewsSerializer(news, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def news_count(request):
    count = News.objects.count()
    return Response({'total_news_sscraped': count})