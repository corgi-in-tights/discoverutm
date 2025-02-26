from django.urls import path

from . import views

urlpatterns = [
    path("get/", views.get_posts, name="post-get"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("update/", views.PostUpdateView.as_view(), name="post-update"),
    path("delete/", views.PostDeleteView.as_view(), name="post-delete"),
]
