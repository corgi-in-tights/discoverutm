from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("posts/", views.HomePageView.as_view(), name="home"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="detail"),
]
