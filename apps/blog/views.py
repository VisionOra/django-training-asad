from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.db import models

from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample

from .models import Post, Category
from .forms import PostForm
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


# ─────────────────────────────────────────────
#  HTML VIEWS
# ─────────────────────────────────────────────

def post_list(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.status == 'draft' and post.author != request.user:
        raise Http404
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


# ─────────────────────────────────────────────
#  API — CATEGORIES
# ─────────────────────────────────────────────

_category_example = {
    "id": 1,
    "name": "Technology",
}

@extend_schema_view(
    list=extend_schema(
        tags=["Categories"],
        summary="List all categories",
        description="Returns a list of all blog post categories.",
        operation_id="categories_list",
        examples=[OpenApiExample("Response", value=[_category_example], response_only=True, status_codes=["200"])],
    ),
    retrieve=extend_schema(
        tags=["Categories"],
        summary="Get a category",
        description="Returns a single category by ID.",
        operation_id="categories_retrieve",
        examples=[OpenApiExample("Response", value=_category_example, response_only=True, status_codes=["200"])],
    ),
    create=extend_schema(
        tags=["Categories"],
        summary="Create a category",
        description="Creates a new category. Requires authentication.",
        operation_id="categories_create",
        examples=[
            OpenApiExample("Request", value={"name": "Technology"}, request_only=True),
            OpenApiExample("Response", value=_category_example, response_only=True, status_codes=["201"]),
        ],
    ),
    update=extend_schema(
        tags=["Categories"],
        summary="Update a category",
        operation_id="categories_update",
    ),
    partial_update=extend_schema(
        tags=["Categories"],
        summary="Partially update a category",
        operation_id="categories_partial_update",
    ),
    destroy=extend_schema(
        tags=["Categories"],
        summary="Delete a category",
        description="Permanently deletes a category.",
        operation_id="categories_delete",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ─────────────────────────────────────────────
#  API — POSTS
# ─────────────────────────────────────────────

_post_example = {
    "id": 1,
    "title": "Getting Started with Django",
    "body": "Django is a high-level Python web framework...",
    "author": "john_doe",
    "category": {"id": 1, "name": "Technology"},
    "status": "published",
    "created_at": "2026-07-01T10:00:00Z",
    "updated_at": "2026-07-01T10:00:00Z",
}

@extend_schema_view(
    list=extend_schema(
        tags=["Posts"],
        summary="List all posts",
        description=(
            "Returns all published posts. Authenticated users also see their own drafts."
        ),
        operation_id="posts_list",
        examples=[OpenApiExample("Response", value=[_post_example], response_only=True, status_codes=["200"])],
    ),
    retrieve=extend_schema(
        tags=["Posts"],
        summary="Get a post",
        description="Returns a single post by ID. Draft posts are only visible to their author.",
        operation_id="posts_retrieve",
        examples=[OpenApiExample("Response", value=_post_example, response_only=True, status_codes=["200"])],
    ),
    create=extend_schema(
        tags=["Posts"],
        summary="Create a post",
        description="Creates a new blog post. The authenticated user is automatically set as the author.",
        operation_id="posts_create",
        examples=[
            OpenApiExample(
                "Request",
                value={
                    "title": "Getting Started with Django",
                    "body": "Django is a high-level Python web framework...",
                    "category_id": 1,
                    "status": "draft",
                },
                request_only=True,
            ),
            OpenApiExample("Response", value=_post_example, response_only=True, status_codes=["201"]),
        ],
    ),
    update=extend_schema(
        tags=["Posts"],
        summary="Update a post",
        description="Fully updates a post. Only the author can update their own posts.",
        operation_id="posts_update",
    ),
    partial_update=extend_schema(
        tags=["Posts"],
        summary="Partially update a post",
        description="Updates one or more fields of a post. Only the author can update their own posts.",
        operation_id="posts_partial_update",
    ),
    destroy=extend_schema(
        tags=["Posts"],
        summary="Delete a post",
        description="Permanently deletes a post. Only the author can delete their own posts.",
        operation_id="posts_delete",
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = Post.objects.select_related("author", "category")
        if self.request.user.is_authenticated:
            return qs.filter(
                models.Q(status="published") | models.Q(author=self.request.user)
            )
        return qs.filter(status="published")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
