from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name='get-routes'),
    path('news/', views.list_news, name='list-news'),
    path('news/<str:pk>/', views.get_news, name='get-news'),
    path('news-count/', views.news_count, name='news_count'),
]
