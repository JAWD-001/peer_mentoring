from django.urls import path

from .views import search

app_name = "search"

urlpatterns = [
    path("results/", search, name="results"),
]
