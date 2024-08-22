from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
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
        news = News.objects.all().order_by('id')

        if tags:
            for tag in tags:
                news = news.filter(tags__label=tag)

        paginator = PageNumberPagination()
        paginated_news = paginator.paginate_queryset(news, request)

        serializer = NewsSerializer(paginated_news, many=True)
        return paginator.get_paginated_response(serializer.data)


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
