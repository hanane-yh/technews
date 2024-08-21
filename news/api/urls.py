from django.urls import path
from .views import GetRoutesView, ListNewsView, GetNewsView, NewsCountView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', GetRoutesView.as_view(), name='get-routes'),
    path('news/', ListNewsView.as_view(), name='list-news'),
    path('news/<str:pk>/', GetNewsView.as_view(), name='get-news'),
    path('news-count/', NewsCountView.as_view(), name='news-count'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

