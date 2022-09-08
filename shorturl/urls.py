from django.urls import path
from . import views

urlpatterns = [
    path("list_create_short_url", views.ListCreateShortUrl.as_view(),
         name="list_create_short_url"),
]
