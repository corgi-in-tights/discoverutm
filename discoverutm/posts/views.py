import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .exceptions import InvalidFilterParameterError
from .filter import filter_posts
from .filter import get_filter_parameters
from .forms import PostForm
from .models import Post
from .serializers import PostSerializer


def home_page_view(request):
    try:
        params = get_filter_parameters(request)
    except InvalidFilterParameterError as e:
        return Response(e.message, status=e.status)

    posts = filter_posts(**params)
    context = {"posts": posts}

    return render(request, "posts/home.html", context)


@login_required
def post_form_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.instance.author = request.user

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("posts:home"))

    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {"form": form})

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

@api_view(["GET"])
def get_posts(request):
    try:
        params = get_filter_parameters(request)
    except InvalidFilterParameterError as e:
        return Response(e.message, status=e.status)

    posts = filter_posts(**params)
    serializer = PostSerializer(posts, many=True, context={"request": request})

    return Response(serializer.data)


class PostCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            serializer = PostSerializer(data=data, context={"request": request})

            if serializer.is_valid():
                post = serializer.save()
                return JsonResponse({"message": "Post created successfully", "id": post.id}, status=201)

            return JsonResponse({"error": serializer.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:  # noqa: BLE001
            return JsonResponse({"error": str(e)}, status=500)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "description", "start_date", "end_date", "location"]

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return JsonResponse({"error": "You are not the author of this post."}, status=403)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:home")

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return JsonResponse({"error": "You are not the author of this post."}, status=403)
        return super().dispatch(request, *args, **kwargs)


