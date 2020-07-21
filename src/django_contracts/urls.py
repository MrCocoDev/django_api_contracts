from django.urls import path

from .discovery import views

urlpatterns = [
    path('^(?P<url>.*)/$', views.http_discovery_view, name='http_discovery_api'),
]
