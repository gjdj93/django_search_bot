from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("<int:pk>", views.view, name="view"),
    path("<int:pk>/update", views.UserUpdate.as_view(), name="update"),
    path("change_password", views.user_change_pass, name="change_password"),
]
