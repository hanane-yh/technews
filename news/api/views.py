from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from news.models import News
from .serializers import NewsSerializer

class GetRoutesView(APIView):
    """
    Returns a list of available API routes.

    It returns a list of routes that users can access to interact with the news data.

    Returns:
        Response: A list of strings, each representing an API route.
    """

    def get(self, request):
        routes = [
            'GET /api',
            'GET /api/news',
            'GET /api/news/:id',
            'GET /api/news/news-count'
        ]
        return Response(routes)


class ListNewsView(APIView):
    """
    Retrieves a list of news articles, optionally filtered by tags.

    This view fetches all news articles stored in the database. If one or
    more tags are provided as query parameters, the results are filtered
    to include only those news articles that are associated with the given tags.

    Query Parameters:
        tag (list of str, optional): A list of tags to filter the news articles by.

    Returns:
        Response: A serialized list of news articles, filtered by the provided tags if any.
    """
    serializer_class = NewsSerializer
    def get(self, request):
        tags = request.query_params.getlist('tag', None)
        if tags:
            news = News.objects.all()
            for tag in tags:
                news = news.filter(tags__label=tag)
        else:
            news = News.objects.all()

        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetNewsView(APIView):
    """
    Retrieves the details of a specific news article by its primary key.

    This view fetches a single news article based on the provided primary key (pk).
    If the news article with the given pk does not exist, a 404 error is returned.

    Parameters:
        pk (str): The primary key of the news article to be retrieved.

    Returns:
        Response: A serialized representation of the requested news article.
    """

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, many=False)
        return Response(serializer.data)


class NewsCountView(APIView):
    """
    Retrieves the total count of news articles in the database.

    This view returns the total number of news articles that have been
    scraped and stored in the database.

    Returns:
        Response: A dictionary containing the total count of news articles.
    """
    serializer_class = NewsSerializer
    def get(self, request):
        count = News.objects.count()
        return Response({'total_news_scraped': count})
