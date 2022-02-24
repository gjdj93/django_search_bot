from django.urls import path

from . import views

app_name = "searches"

urlpatterns = [
    path("create", views.create, name="create"),
    path("<int:pk>/view", views.view, name="view"),
    path("<int:pk>/update", views.SearchUpdate.as_view(), name="update"),
    path("<int:pk>/delete", views.delete, name="delete"),
    path("<int:pk>/found", views.found, name="found"),
]
