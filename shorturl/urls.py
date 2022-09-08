from django.urls import path
from . import views

urlpatterns = [
    path("create_short_url", views.CreateShortUrl.as_view(),
         name="create_short_url"),
    path("", views.FetchShortUrl.as_view(),
         name="fetch_short_url"),
]
