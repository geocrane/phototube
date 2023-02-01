from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from phototube.settings import POSTS_ON_PAGE


def create_pages(request, post_list):
    return Paginator(post_list, POSTS_ON_PAGE).get_page(
        request.GET.get("page")
    )


def index(request):
    return render(
        request,
        "posts/index.html",
        {"page_obj": create_pages(request, Post.objects.all())},
    )


def group_posts(request, group_name):
    group = get_object_or_404(Group, slug=group_name)
    return render(
        request,
        "posts/group_list.html",
        {
            "group": group,
            "page_obj": create_pages(request, group.posts.all()),
        },
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = (
        request.user.username != username
        and request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=author).exists()
    )
    return render(
        request,
        "posts/profile.html",
        {
            "author": author,
            "page_obj": create_pages(request, author.posts.all()),
            "following": following,
        },
    )


def post_detail(request, post_id):
    return render(
        request,
        "posts/post_detail.html",
        {"post": get_object_or_404(Post, id=post_id), "form": CommentForm()},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, "posts/create_post.html", {"form": form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("posts:profile", username=post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id=post_id)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if not form.is_valid():
        return render(request, "posts/create_post.html", {"form": form})
    form.save(request.POST)
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    return render(
        request,
        "posts/follow.html",
        {
            "page_obj": create_pages(
                request,
                Post.objects.filter(author__following__user=request.user.id),
            )
        },
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    get_object_or_404(
        Follow, user=request.user, author__username=username
    ).delete()
    return redirect("posts:profile", username=username)
