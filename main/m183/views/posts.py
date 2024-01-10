from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Post, Comment
from ..forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test



def home(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'home.html', {'posts': posts})

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'posts/dashboard.html', {'user_posts': user_posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    if post.status == 'published' or (post.status == 'hidden' and (request.user == post.author or request.user.is_staff)) or (post.status == 'deleted' and request.user.is_staff):
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        return render(request, 'posts/post.html', {'post': post, 'comments': comments, 'form': form})
    else:
        return redirect('home')
