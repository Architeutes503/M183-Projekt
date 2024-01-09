from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Post, Comment


def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'home.html', {'posts': posts})


def dashboard(request):
    return render(request, 'posts/dashboard.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'posts/post.html', {'post': post, 'comments': comments})
